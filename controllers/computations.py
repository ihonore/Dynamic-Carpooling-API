import requests

from config.database import offers_collection
from config.database import demands_collection
from models.offers import offers
from models.demands import demands
from schema.offers import list_serial
from schema.demands import list_serial


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
    
def export_locations(offers: list, demands:list) -> list:
    offers = list_serial(offers_collection.find())
    demands = list_serial(demands_collection.find())
    reqs = offers + demands
    
    locations = []
    
    for req in reqs:
        for itin in req.itinerary:
            locations.append(itin.origin)
            locations.append(itin.destination)
            for via in itin.vias:
                locations.append(via)
                
    return locations
    

def build_distance_matrix(locations) -> list[list]:
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