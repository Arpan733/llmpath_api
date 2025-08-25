import spacy
import re
import requests
import api
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

def extract_locations(query, exclude=[]):
    doc = nlp(query)
    locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FACILITY"] and ent.text not in exclude]
    return locations

def extract_waypoints(query):
    waypoint_patterns = [
        r"stop at ([\w\s]+)",
        r"night stay (?:at|in) ([\w\s,]+)",
        r"via ([\w\s,]+)",
        r"quick stop at ([\w\s]+)"
    ]

    waypoints = []

    for pattern in waypoint_patterns:
        matches = re.findall(pattern, query.lower())
        for match in matches:
            extracted_points = [point.strip() for point in re.split(r",|and", match)]
            waypoints.extend(extracted_points)

    return waypoints

def extract_distance_constraints(query):
    pattern = r"rest stops every (\d+ ?(?:miles|mile|km|kilometers))"
    matches = re.findall(pattern, query.lower())
    return matches

def extract_time_constraints(query):
    doc = nlp(query)

    times = [ent.text for ent in doc.ents if ent.label_ in ["TIME", "DATE"]]

    duration_pattern = r"(\d+\s?(?:minutes|minute|mins|min|hours|hour|hrs|hr))"
    durations = re.findall(duration_pattern, query.lower())

    constraints = {
        "times": times,
        "durations": durations
    }
    return constraints

def extract_intents(query: str) -> list:
    query_lower = query.lower()
    detected_intents = []

    intent_keywords = {
        "Basic Navigation": ["navigate", "route", "direction", "way to reach", "go to"],
        "Multi-Stop": ["multi-stop", "stops at", "via", "passing through", "multiple stops", "with stops"],
        "Time-Constrained": ["arrive by", "reach by", "leave at", "depart at", "by", "before", "after", "sharp"],
        "Traffic-Aware": ["avoid traffic", "traffic-free", "least traffic", "no congestion"],
        "Scenic Routing": ["scenic", "beautiful", "picturesque", "scenery"],
        "Fuel-Efficient": ["fuel-efficient", "save fuel", "economic route"],
        "Avoiding Tolls": ["avoid tolls", "no tolls", "without toll"],
        "Avoiding Highways": ["avoid highways", "no highways", "without highways"],
        "Weather-Based": ["weather", "rain", "snow", "storm", "avoid weather"],
        "EV Charging": ["ev charging", "electric charging", "charging stations", "ev stops"],
        "Emergency Routing": ["hospital", "emergency", "urgent care", "immediately"],
        "Parking Availability": ["parking", "park near", "where can i park"],
        "Shortest": ["shortest", "quickest", "fastest"],
        "Rest Stop": ["rest stop", "break every", "rest every", "stop every"],
        "Night Stay": ["night stay", "overnight", "stay in", "stay at"]
    }

    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if re.search(r'\\b' + re.escape(keyword) + r'\\b', query_lower):
                detected_intents.append(intent)
                break

    return detected_intents

def extract_pincode(start_location):
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        "q": start_location,
        "apiKey": api.here_appid
    }

    response = requests.get(url, params=params)
    data = response.json()
    items = data.get("items", [])

    if items:
        address = items[0].get("address", {})
        return address.get("postalCode")

    return None

def extract_start_end_locations(query):
    start_match = re.search(r"from ([\w\s]+?) to", query.lower())
    end_match = re.search(r"to ([\w\s]+?)(,|\.| with| but| and|$)", query.lower())

    start_location = start_match.group(1).strip() if start_match else "current location"
    end_location = end_match.group(1).strip() if end_match else None

    return start_location, end_location

def structured_output(query):
    start_location, end_location = extract_start_end_locations(query)
    locations = extract_locations(query, exclude=[start_location, end_location])
    waypoints = extract_waypoints(query)
    unique_waypoints = [w for w in waypoints if w not in locations]

    return {
        "intents": extract_intents(query),
        "start_location": start_location,
        "end_location": end_location,
        "locations": locations,
        "waypoints": unique_waypoints,
        "pincode": extract_pincode(start_location),
        "distance_constraints": extract_distance_constraints(query),
        "time_constraints": extract_time_constraints(query)
    }

# queries = [
#     "Plan a long road trip from New York to Los Angeles with rest stops every 300 miles and a night stay in Chicago and Denver.",
#     "Find the shortest route from my house to the airport with a quick stop at a nearby ATM.",
#     "Show me a scenic drive from San Francisco to Yosemite National Park with a stop at a famous viewpoint.",
#     "Navigate from Dallas to Austin avoiding tolls and highways, prefer fuel-efficient route with EV charging every 150 miles.",
#     "I need to urgently reach a hospital from my office due to heavy snow and avoid traffic.",
#     "Plan a trip from Seattle to Portland, include scenic views, parking availability near downtown, and rest stops every 100 miles."
# ]

# l = []

# for q in queries:
#     l.append(structured_output(q))

# print(l)