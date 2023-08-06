import sqlalchemy
from sqlalchemy import create_engine
from supextend.config import Config
from supextend.exceptions import DbConnectionFailedError, TableDoesNotExistError


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [Config.schema_name]
    else:
        return True


def schema_exists(schema=Config.schema_name):
    try:
        engine = create_engine(Config.database_url)
        conn = engine.connect()
    except sqlalchemy.exc.OperationalError as e:
        raise DbConnectionFailedError(extra=e)
    if not conn.dialect.has_schema(conn, schema):
        return False
    return True


def table_exists(table):
    engine = create_engine(Config.database_url)
    conn = engine.connect()
    if not conn.dialect.has_table(conn, table):
        raise TableDoesNotExistError(extra=f"__tablename__: {table}")
    return True
