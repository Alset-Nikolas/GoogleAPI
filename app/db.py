from models import Base, engine
from sqlalchemy_utils import database_exists, create_database, drop_database


def init_db() -> None:
    """
    Создаем таблицы
    """
    try:
        drop_database(engine.url)
    except:
        print("db_table  delete to upgrade")

    print("init data base")
    if not database_exists(engine.url):
        print("create db_table ")
        create_database(engine.url)
        Base.metadata.create_all(engine)
        return
    print("db_table exist")
