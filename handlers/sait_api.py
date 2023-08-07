from typing import Dict

import requests


# Общий метод для запросов к API
def _make_response(method: str, url: str, headers: Dict, querystring: Dict,
                  timeout: int = 10, success=200):
	response = requests.request(
			method=method,
			url=url,
			headers=headers,
			params=querystring,
			timeout=timeout
	)

	status_code = response.status_code

	if status_code == success:
		return response

	return status_code


# Методы для запросов к API по разным опциям самого API
# В методах формируются параметры запроса к API после чего вызывается общий метод _make_response
def _get_airports_by_ip_address_geolocation(method: str, url: str, headers: Dict, params: Dict,
		ip_user: str, radius_km: int, limit_search_airport: int, func=_make_response):
	params["q"] = ip_user
	params["radiusKm"] = str(radius_km)
	params["limit"] = str(limit_search_airport)
	response = func(method, url, headers=headers, querystring=params)

	return response


def _get_airports_by_free_text(method: str, url: str, headers: Dict, params: Dict,
		city_search: str, limit_search_airport: str, func=_make_response):
	params["q"] = city_search
	params["limit"] = str(limit_search_airport)
	response = func(method, url, headers=headers, querystring=params)

	return response


def _get_flight_status_with_date(method: str, url: str, headers: Dict, params: Dict,
		func=_make_response):
	response = func(method, url, headers=headers, querystring=params)

	return response


# Класс интерфейса для работы с запросами к API
class SiteAPIInterface:
	def __init__(self) -> None:
		self.airports_ip = _get_airports_by_ip_address_geolocation
		self.airports_text = _get_airports_by_free_text
		self.flight_status = _get_flight_status_with_date

	def airports_ip(self):
		return self.airports_ip

	def airports_text(self):
		return self.airports_text

	def flight_status(self):
		return self.flight_status


if __name__ == "__main__":
	_make_response()
	_get_airports_by_ip_address_geolocation()
	_get_airports_by_free_text()
	_get_flight_status_with_date()
	SiteAPIInterface()
