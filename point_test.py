import googlemaps
import folium

# Your Google API Key
gmaps = googlemaps.Client(key='AIzaSyCFfNMPGWRnN8OF5fvnPa_ZnChdvjwqOXc')

# List of locations
locations = ["Manchester Piccadilly station", "Piccadilly Plaza", "Portland Street"]  # Add all locations here

# Fetch latitude and longitude for each location
coords = []
for location in locations:
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
        coords.append((lat, lng))
    else:
        print(f"Could not get geocode for location: {location}")

# Check if coordinates are available
if coords:
    # Create a map
    map = folium.Map(location=[53.4808, -2.2426], zoom_start=13)  # Manchester's approximate central coordinates

    # Plot the points and lines
    for i in range(len(coords) - 1):
        folium.Marker(coords[i]).add_to(map)
        folium.PolyLine([coords[i], coords[i+1]], color="blue").add_to(map)

    # Save to an HTML file
    map.save("map.html")
else:
    print("No coordinates available to plot the map.")
