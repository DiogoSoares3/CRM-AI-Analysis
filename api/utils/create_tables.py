from core.configs import settings
from core.database import engine


def create_tables() -> None:
    import models.__all_models

    print('Creating tables.')

    with engine.begin() as conn:
        settings.DBBaseModel.metadata.drop_all(bind=conn)
        settings.DBBaseModel.metadata.create_all(bind=conn)

    print("Tables successfully created!")


if __name__ == '__main__':
    create_tables()
