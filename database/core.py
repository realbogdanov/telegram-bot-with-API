from database.CRUD import DBFacade
from database.common.models import db, Airports, Airplanes

# Создание таблиц в базе данных
db.connect()
db.create_tables([Airports])
db.create_tables([Airplanes])

# Создание экземпляра класса DBFacade с фасадом для работы с базой данных
crud = DBFacade

if __name__ == "__main__":
	crud()
