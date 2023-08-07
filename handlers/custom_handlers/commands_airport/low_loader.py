from config_data.config import SiteSettings

from handlers.sait_api import SiteAPIInterface

site = SiteSettings()

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
}

url = "https://{}/airports/search/ip".format(site.host_api)
params = {"q":"123.123.123.123","radiusKm":"50","limit":"10","withFlightInfoOnly":"true"}

site_api = SiteAPIInterface()

if __name__ == "__main__":
	site_api()
