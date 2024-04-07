from app.core.database import AsyncSession
from app.models.request_info import RequestInfo
from app.schemas.facebook_data import RequestInfoCreate


async def create_request_info(new_request_info: RequestInfoCreate) -> RequestInfo:
    print(new_request_info)
    new_request_info = new_request_info.model_dump()
    print(new_request_info)
    return new_request_info
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