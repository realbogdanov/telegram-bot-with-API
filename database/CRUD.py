from typing import Dict, List, TypeVar, Any

from peewee import ModelSelect

from database.common.models import db, ModelBase


T = TypeVar('T')


# Класс для работы с базой данных
class DBFacade:
	def record_data(self, model: T, *data: List[Dict]) -> None:
		with db.atomic():
			model.insert_many(*data).execute()


	def reading_all_data(self, model: T, *columns: ModelBase) -> ModelSelect:
		with db.atomic():
			response = model.select(*columns)
			return response



if __name__ == "__main__":
	DBFacade()
