import os
import json
from internal import constants
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from internal.writer_abstract import WriterAbstract

class PostgreSQLWriter(WriterAbstract):
    def __init__(self, db_url):
    #def __init__(self, username, password, host, port, database_name):
        #engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')
        engine = create_engine(db_url)
        # 資料庫不存在則建立
        if not database_exists(engine.url):
            create_database(engine.url)
        # FIXME add options on/off 存在則刪除並重新建立
        # else:
        #     drop_database(engine.url)
        #     create_database(engine.url)

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

    def finish(self):
        self.conn.close()
        self.session.close()
