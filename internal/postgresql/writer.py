import json
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from internal.writer_abstract import WriterAbstract


class PostgreSQLWriter(WriterAbstract):
    def __init__(self, db_url, recreate_target):
        engine = create_engine(db_url)

        if not database_exists(engine.url):
            create_database(engine.url)
        elif recreate_target:
            drop_database(engine.url)
            create_database(engine.url)

        self.engine = engine
        self.conn = engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def table_writer(self, data):
        sql_statement = data['content']
        if sql_statement.strip():
            transaction = self.conn.begin()
            try:
                self.conn.execute(text(sql_statement.strip()))
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

    def sp_writer(self, data):
        sql_statement = data['content']
        if sql_statement.strip():
            transaction = self.conn.begin()
            try:
                self.conn.execute(text(sql_statement.strip()))
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

    def trigger_writer(self, data):
        sql_statement = data['content']
        if sql_statement.strip():
            transaction = self.conn.begin()
            try:
                self.conn.execute(text(sql_statement.strip()))
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

    def data_writer(self, data):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        json_data  = json.loads(data['content'])
        table_name = data['table_name']
        if table_name in metadata.tables:
            table = metadata.tables[table_name]
            for row in json_data:
                self.session.execute(table.insert().values(row))
            self.session.commit()

    def manifest_writer(self, driver):
        pass

    def finish(self):
        self.conn.close()
        self.session.close()
