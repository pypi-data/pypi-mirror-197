import ray
import pandas as pd
from sqlalchemy import create_engine

from aib._private.utils.utils import init_check
from aib._private.utils.VO import MysqlInfoVO


def range(n: int, parallelism: int = -1) -> ray.data.Dataset:
    try:
        init_check()
    except Exception as exc:
        raise exc
    ds = ray.data.range(n=n, parallelism=parallelism)
    return ds


def read_csv(paths: str | list[str], parallelism: int = -1) -> ray.data.Dataset:
    try:
        init_check()
    except Exception as exc:
        raise exc
    ds = ray.data.read_csv(paths=paths, parallelism=parallelism)
    return ds


def read_mysql(db_info: MysqlInfoVO, table: str) -> pd.DataFrame:
    connection_str = "mysql+mysqlconnector://" + db_info.USER + ':' + db_info.PASSWORD + '@' + \
                     db_info.IP + ':' + db_info.PORT + '/' + db_info.DB
    engine = create_engine(connection_str, convert_unicode=True)
    conn = engine.connect()
    data = pd.read_sql_table(table, conn)
    return data

