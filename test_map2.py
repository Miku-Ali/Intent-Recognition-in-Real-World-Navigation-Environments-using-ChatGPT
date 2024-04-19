import googlemaps
from datetime import datetime
import html
import re

def Tokenlization(raw_html):
    """Remove HTML tags and unescape HTML entities."""
    clean_text = re.sub('<.*?>', '', raw_html)  # Remove HTML tags
    return html.unescape(clean_text)  # Convert HTML entities to their corresponding characters

def extract_locations(directions):
    """Extract unique location names from directions, excluding duplicates and refining extraction."""
    locations = []
    seen = set()  # Set to track seen locations

    location_pattern = re.compile(r'\b(?:toward|onto|to|at|past|before|after|along)\s+([\w\s/\-]+?)(?:\s+(?:Continue to follow|stay on)|\s*/|\s*\-|$)')

    for direction in directions:
        # Preprocessing to replace certain phrases before applying regex
        direction = re.sub(r'\b(stay on)\b\s+', '', direction)

        matches = location_pattern.findall(direction)
        for match in matches:
            location_name = match.strip()
            # Further cleaning to refine location name extraction
            location_name = re.sub(r'/.*', '', location_name)  # Remove everything after a slash
            location_name = re.sub(r'\-.*', '', location_name)  # Remove everything after a hyphen
            if location_name and location_name not in seen:  # Check if the location is not a duplicate
                seen.add(location_name)
                locations.append(location_name)
    return locations

def get_route(api_key, origin, destination):
    # Create a client
    gmaps = googlemaps.Client(key=api_key)

    # Request directions
    now = datetime.now()
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="driving",
                                         departure_time=now)
    
    cleaned_instructions = []
    location_names = []
    
    if directions_result:
        for step in directions_result[0]['legs'][0]['steps']:
            raw_instruction = step['html_instructions']
            cleaned_instruction = Tokenlization(raw_instruction)
            cleaned_instructions.append(cleaned_instruction)

        location_names = extract_locations(cleaned_instructions)

        return directions_result, cleaned_instructions, location_names
    else:
        print("No route could be found between the specified points.")
        return None, None, None

api_key = 'AIzaSyCFfNMPGWRnN8OF5fvnPa_ZnChdvjwqOXc'

# start point and end point 
origin = "Manchester Piccadilly station"
destination = "Manchester Kilburn Building"

route, cleaned_instructions, location_names = get_route(api_key, origin, destination)

if location_names:
    for location in location_names:
        print(location)
