import json
from datetime import datetime
from sqlalchemy import create_engine, MetaData,  inspect, text
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from internal.exporter_abstract import ExporterAbstract

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class PostgreSQLExporter(ExporterAbstract):
    def __init__(self, db_url):
    #def __init__(self, username, password, host, port, database_name):
        #engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')
        engine = create_engine(db_url)
        if not database_exists(engine.url):
            print('資料庫不存在')
            exit()
        self.engine = engine
        self.conn = engine.connect()
        self.inspector = inspect(self.engine) # 建立 Inspector，用於取得資料庫結構資訊

    # 遞迴處理，按照依賴順序加入
    def process_dependency_table(self, table_name, dependency_order):
        # 取得表的依賴關係
        foreign_keys = self.inspector.get_foreign_keys(table_name)

        # 遞迴處理每個依賴
        for foreign_key in foreign_keys:
            dependent_table = foreign_key['referred_table']
            if dependent_table not in dependency_order:
                self.process_dependency_table(dependent_table)

        # 將當前的表加到列表中
        dependency_order.append(table_name)

    def export(self, writer):
        self.table_exporter(writer.table_writer)
        self.sp_exporter(writer.sp_writer)
        self.trigger_exporter(writer.trigger_writer)
        self.data_exporter(writer.data_writer)
        self.finish()
        writer.finish()

    def table_exporter(self, callback):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        inspector = inspect(self.engine)

        # 取得資料庫中的所有表格
        tables = self.inspector.get_table_names()

        # 空的列表存依賴順序
        dependency_order = []

        # 遞迴處理，按照依賴順序加到列表中
        for table in tables:
            if table not in dependency_order:
                self.process_dependency_table(table, dependency_order)

        for i, table_name in enumerate(dependency_order):
            content = ""
            table = metadata.tables[table_name]
            create_table_statement = CreateTable(table).compile(self.engine).string.strip()
            content += str(create_table_statement) + ';\n\n'
            file_name = f'{i+1:02d}_{table_name}.sql'

            for index in table.indexes:
                unique = 'UNIQUE ' if index.unique else ''
                index_name = f'"{index.name}"'
                index_columns = ', '.join(f'"{column_name}"' for column_name in index.columns.keys())
                index_statement = f"CREATE {unique}INDEX IF NOT EXISTS {index_name} ON \"{table_name}\" ({index_columns});"
                content += index_statement + '\n'

            callback({'file_name': file_name, 'content': content})

    def sp_exporter(self, callback):
        query = text("""
            SELECT
                p.proname AS procedure_name,
                pg_get_functiondef(p.oid) AS procedure_definition
            FROM
                pg_catalog.pg_proc p
            WHERE
                p.pronamespace = (SELECT oid FROM pg_catalog.pg_namespace WHERE nspname = 'public')
        """)
        result = self.conn.execute(query)
        
        for row in result:
            content = ""
            procedure_name = row[0]
            procedure_definition = row[1]
            file_name = f"{procedure_name}.sql"
            content += procedure_definition
            callback({'file_name': file_name, 'content': content})

    def trigger_exporter(self, callback):
        query = text("""
            SELECT 
                tgname AS table_name,
                tgname AS trigger_name,
                pg_get_triggerdef(oid) AS trigger_definition
            FROM pg_trigger
            WHERE tgrelid IN (
                SELECT oid
                FROM pg_class
                WHERE relkind = 'r'
            )
            AND tgname NOT LIKE 'RI_ConstraintTrigger%%'
        """)
        result = self.conn.execute(query)

        for row in result:
            content = ""
            table_name, trigger_name, trigger_definition = row
            file_name = f'{table_name}_{trigger_name}.sql'
            content += trigger_definition + ';\n'
            callback({'file_name': file_name, 'content': content})

    def data_exporter(self, callback):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        # 取得資料庫中的所有表格
        tables = self.inspector.get_table_names()

        # 空的列表存依賴順序
        dependency_order = []

        # 遞迴處理，按照依賴順序加到列表中
        for table in tables:
            if table not in dependency_order:
                self.process_dependency_table(table, dependency_order)

        for i, table_name in enumerate(dependency_order):
            table = metadata.tables[table_name]
            rows = session.query(table).all()

            data = []
            content = ""
            for row in rows:
                data.append(dict(row._asdict()))

            json_data = json.dumps(data, indent=4, cls=CustomJSONEncoder, ensure_ascii=False)

            file_name = f'{i + 1:02d}_{table_name}.json'
            content += json_data

            callback({'table_name': table_name, 'file_name': file_name, 'content': content})

        session.close()

    def finish(self):
        self.conn.close()

