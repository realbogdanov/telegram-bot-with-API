from config_data.config import SiteSettings
from handlers.sait_api import SiteAPIInterface

# Генерирует url для запроса к API сайта
def generate_url(flight_number: str, data_search: str) -> str:
	"""Генерирует url для запроса к API сайта"""
	url = "https://{host}/flights/number/{flight_number}/{data_search}".format(host=site.host_api,
	                                                                           flight_number=flight_number,
	                                                                           data_search=data_search)
	return url

site = SiteSettings()

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
}

params = {"withAircraftImage":"true","withLocation":"true"}

site_api = SiteAPIInterface()

if __name__ == "__main__":
	site_api()
