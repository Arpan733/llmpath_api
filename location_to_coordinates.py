import requests
import api

def geocode_location(location_name=None, postal_code=None):
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        "apiKey": api.here_apikey
    }

    if location_name:
        params["q"] = location_name

    if postal_code:
        params["in"] = f"postalCode:{postal_code}"

    response = requests.get(url, params=params)
    items = response.json().get("items", [])

    if items:
        position = items[0].get("position", {})
        address = items[0].get("address", {})
        
        return {
            "lat": position.get("lat"),
            "lon": position.get("lng"),
            "postalCode": address.get("postalCode"),
            "countryCode": address.get("countryCode")
        }
    
    return None

# l = ["university of texas at arlington", "university of houston", "dallas", "london", "london business school", "university of queensland", "windsor", "surat"]

# for i in l:
#     print(geocode_location(i))