import requests
import sys

from config.database import offers_collection, demands_collection
from schema.offers import list_serial as list_serial_offers
from schema.demands import list_serial as list_serial_demands

# Generate an unique id to each location
def generate_unique_id(coord) -> str:
    return f"{coord['latitude']}_{coord['longitude']}"

# Build a list of all locations with their unique id
def add_ids_to_locations(locations) -> list:
    result = []

    for location in locations:
        location_id = generate_unique_id(location['coord'])
        result.append({'id': location_id}, **location )
        
    return result

# Compute the distance and duration of two coordinates
def get_osrm_route(coord1, coord2):
    # Open Source Route Machine API (Computation of distance and duration)
    # Format des coordonnées : [longitude, latitude]
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1[0]},{coord1[1]};{coord2[0]},{coord2[1]}"
    response = requests.get(url)
    
    if response.status_code == 200:
        route_data = response.json()
        return route_data['routes'][0] if route_data['code'] == 'Ok' and len(route_data['routes']) > 0 else None
    else:
        return None
    
# Extract every locations (origin, destination and vias) of each itinerary either for offer or demand
def extract_locations() -> list:
    offers = list_serial_offers(offers_collection.find())
    demands = list_serial_demands(demands_collection.find())
    reqs = offers + demands
    
    locations = []
    
    for req in reqs:
        for itin in req.itinerary:
            locations.append(itin.origin)
            locations.append(itin.destination)
            for via in itin.vias:
                locations.append(via)
                
    return locations
    

# Build the origin-destination matrix
def build_matrix(locations) -> list[list]:
    n = len(locations)
    distance_matrix = [[None] * n for _ in range(n)]
        
    for i in range(n):
        for j in range(n):
            if i != j:
                route_info = get_osrm_route(locations[i].coordinates, locations[j].coordinates)
                
                if route_info:
                    distance_matrix[i][j] = {
                        'distance': round(route_info['distance'] / 1000, 2), # Convert in km
                        'duration': round(route_info['duration'] / 60, 2), # Convert in mn
                    }
    
    return distance_matrix

# Extract all requests according to their type
"""def extract_requests() :
    offers = list_serial_offers(offers_collection.find())
    demands = list_serial_demands(demands_collection.find())
    reqs = offers + demands
    
    list_OD, list_OP, list_MD, list_MP = []
    
    for req in reqs:
        if req."""
    
    


def computation():   
    all_locations = extract_locations()
    all_locations = add_ids_to_locations(all_locations)
    
    for row in all_locations:
        print(row)
        
    return all_locations

"""

# Filtrer les locations uniques avec les IDs ajoutés
unique_locations = filter_unique_locations(locations_with_ids)

# Afficher les résultats
print_locations(unique_locations)

# Utiliser les locations obtenues précédemment
distance_matrix = build_matrix(unique_locations)

# Afficher la matrice des distances
print("\nMatrice des distances entre les locations:")
for row in distance_matrix:
    print(row)"""