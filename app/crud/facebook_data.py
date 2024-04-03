from app.core.database import AsyncSession
from app.models.facebook_data import FacebookData
from app.schemas.facebook_data import FacebookDataCreate


async def create_facebook_data(new_facebook_data: FacebookDataCreate) -> FacebookData:
    print(new_facebook_data)
    new_facebook_data = new_facebook_data.model_dump()
    print(new_facebook_data)
    return new_facebook_data
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