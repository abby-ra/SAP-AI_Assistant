from backend.config import settings


def get_db_connection_info() -> dict:
    return {
        "engine": settings.db_engine,
        "host": settings.db_host,
        "port": settings.db_port,
        "database": settings.db_name,
        "user": settings.db_user,
    }
