import requests
import api
from location_to_coordinates import geocode_location
import polyline

def get_route_info(structure):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    start_coords = geocode_location(structure.get('start_location'))
    if not start_coords:
        start_coords = geocode_location("University of Texas at Arlington")

    end_coords = geocode_location(structure.get('end_location'))
    if not end_coords:
        end_coords = geocode_location("University of Texas at Dallas")

    params = {
        "origin": f"{start_coords['lat']},{start_coords['lon']}",
        "destination": f"{end_coords['lat']},{end_coords['lon']}",
        "mode": "driving",
        "key": api.google_apikey
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        coords_list = []

        if data.get("routes"):
            route = data["routes"][0]
            leg = route.get("legs", [])[0]

            distance = leg.get("distance", {}).get("value")
            duration = leg.get("duration", {}).get("value")

            encoded_polyline = route.get("overview_polyline", {}).get("points", "")
            try:
                coords = polyline.decode(encoded_polyline)
                coords_list.extend([[lat, lng] for lat, lng in coords])
            except Exception as e:
                print("Error decoding polyline:", e)

            return {
                "distance_meters": distance,
                "duration_seconds": duration,
                "polyline": coords_list
            }
        else:
            return {
                "distance_meters": None,
                "duration_seconds": None,
                "polyline": []
            }
    else:
        print(f"Google Directions API error: {response.status_code}")
        return None
        
# l = [
#         {'intents': [], 'start_location': 'new york', 'end_location': 'los angeles', 'locations': ['New York', 'Los Angeles', 'Chicago', 'Denver'], 'waypoints': ['chicago', 'denver'], 'pincode': '10007', 'distance_constraints': ['300 miles'], 'time_constraints': {'times': ['night'], 'durations': []}},
#         {'intents': [], 'start_location': 'san francisco', 'end_location': 'yosemite national park', 'locations': ['San Francisco'], 'waypoints': ['a famous viewpoint'], 'pincode': '94102', 'distance_constraints': [], 'time_constraints': {'times': [], 'durations': []}},
        # {'intents': [], 'start_location': 'dallas', 'end_location': 'houston', 'locations': ['Dallas'], 'waypoints': [], 'pincode': '75201', 'distance_constraints': [], 'time_constraints': {'times': [], 'durations': []}},
        # {'intents': [], 'start_location': 'houston', 'end_location': 'FWD airport', 'locations': [], 'waypoints': [], 'pincode': None, 'distance_constraints': [], 'time_constraints': {'times': [], 'durations': []}},
        # {'intents': [], 'start_location': 'seattle', 'end_location': 'portland', 'locations': ['Seattle', 'Portland'], 'waypoints': [], 'pincode': '98104', 'distance_constraints': ['100 miles'], 'time_constraints': {'times': [], 'durations': []}},
    # ]

# for i in l:
#     print(get_route_info(i))

# print(get_route_info({'intents': [], 'start_location': 'houston', 'end_location': 'dallas', 'locations': [], 'waypoints': [], 'pincode': '', 'distance_constraints': [], 'time_constraints': {'times': [], 'durations': []}}))
# print(get_route_info({'intents': [], 'start_location': 'dallas', 'end_location': 'houston', 'locations': [], 'waypoints': [], 'pincode': '', 'distance_constraints': [], 'time_constraints': {'times': [], 'durations': []}}))