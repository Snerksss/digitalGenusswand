from data.persistence_manager import PersistenceManager

persistence_manager = PersistenceManager()


async def get_persistence_manager():
    try:
        yield persistence_manager
    finally:
        return
