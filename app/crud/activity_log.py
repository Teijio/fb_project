from app.core.database import AsyncSession
from app.models.activity_log import ActivityLog
from app.schemas.facebook_data import ActivityLogCreate


async def create_activity_log(new_activity_log: ActivityLogCreate) -> ActivityLog:
    db_activity_log = ActivityLog(**new_activity_log.model_dump())
    print(db_activity_log)
    return new_activity_log
    # # Создаём объект модели MeetingRoom.
    # # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    # db_room = MeetingRoom(**new_room_data)

    # # Создаём асинхронную сессию через контекстный менеджер.
    # async with AsyncSessionLocal() as session:
    #     # Добавляем созданный объект в сессию. 
    #     # Никакие действия с базой пока ещё не выполняются.
    #     session.add(db_room)

    #     # Записываем изменения непосредственно в БД. 
    #     # Так как сессия асинхронная, используем ключевое слово await.
    #     await session.commit()

    #     # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    #     await session.refresh(db_room)
    # # Возвращаем только что созданный объект класса MeetingRoom.
    # return db_room 