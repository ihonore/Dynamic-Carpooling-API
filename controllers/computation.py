import os
import requests
import pandas as pd

from datetime import datetime, timedelta
from config.database import offers_collection, demands_collection, users_collection
from schema.offers import list_serial as list_serial_offers
from schema.demands import list_serial as list_serial_demands

from bson import ObjectId

# All location includes origin, destination and vias of demands and offers request
all_locations = []

# Origin-destination matrix computed from all locations
#matrix = []

# List of all requests from offers and demands
list_req = {'od' : [], 'op' : [], 'md' : [], 'mp' : []}
    
# List of solution
solutions = []

# Matrix output to xlsx file
# writer = pd.ExcelWriter('origin-destination_matrix.xlsx', engine = 'xlsxwriter')

# Parse string to datatime
def stringToDateTime(date_str: str)->datetime:
    date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    # Convertir la chaîne en objet datetime
    date_time_obj = datetime.strptime(date_str, date_format)

    # Afficher l'objet datetime
    return date_time_obj

# Extract every locations (origin, destination and vias) of each itinerary either for offer or demand
def extract_locations() -> list:
    offers = list_serial_offers(offers_collection.find())
    demands = list_serial_demands(demands_collection.find())
    reqs = offers + demands
        
    locations = []
    
    for req in reqs:
        locations.append(req['itinerary']['origin'])
        locations.append(req['itinerary']['destination'])
        for via in req['itinerary']['vias']:
            if via != None: locations.append(via)
                
    return locations

# Build a list of all locations with their unique id
def add_ids_to_locations(locations) -> list:
    result = []

    for location in locations:
        location_id = generate_unique_id(location['coordinates'])
        result.append({'id': location_id, **location})  
    return result

# Generate an unique id to each location
def generate_unique_id(coord) -> str:
    return f"{coord[0]}_{coord[1]}" # 0:Long, 1:Lat
    
# filter all locations by unique id in order to remove duplicate
def filter_unique_locations(locations_with_ids):
    unique_ids_set = set()
    unique_locations = []

    for location in locations_with_ids:
        location_id = location['id']
        if location_id not in unique_ids_set:
            unique_ids_set.add(location_id)
            unique_locations.append(location)

    return unique_locations

# Write the locations in xslx file    
def print_locations(locations):
    df1 = pd.DataFrame(locations)
    # df1.to_excel(writer, sheet_name = 'Locations')
    
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location} \n")
        # Write to xlsx file"""

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

# Build the origin-destination matrix
def build_matrix(locations) -> list[list]:
    n = len(locations)
    matrix = [[None] * n for _ in range(n)]
        
    for i in range(n):
        for j in range(n):
            if i != j:
                coord_i = [locations[i]['coordinates'][0], locations[i]['coordinates'][1]]
                coord_j = [locations[j]['coordinates'][0], locations[j]['coordinates'][1]]
                # print(coord_i, coord_j)
                route_info = get_osrm_route(coord_i, coord_j)
                
                if route_info:
                    matrix[i][j] = {
                        'itinerary': f"{locations[i]['location_name']} -> {locations[j]['location_name']}", # Convert in mn
                        'distance': round(route_info['distance'] / 1000, 2), # Convert in km
                        'duration': round(route_info['duration'] / 60, 2), # Convert in mn
                    }
            else: 
                matrix[i][j] = {
                    'itinerary': f"{locations[i]['location_name']} -> {locations[j]['location_name']}", # Convert in mn
                    'distance': 0,
                    'duration': 0, 
                }
                
    # Write in Excel file
    df2 = pd.DataFrame(matrix)
    # df2.to_excel(writer, sheet_name = 'Origin-destination')
    # writer.close()
    
    return matrix

# Extract all requests according to their type
def extract_requests() :
    offers = list_serial_offers(offers_collection.find())
    demands = list_serial_demands(demands_collection.find())
    reqs = offers + demands
        
    fields_to_remove = ['plate_number', 'message', 'created_at']
    
    for req in reqs:
        #print(req)
        # Remove useless fields for algorithm
        for field in fields_to_remove:
            if field in req:
                del req[field]
        
        # Convert Itinerary dict to List
        req['itinerary'] = convert_itinerary_dict_to_list(req['itinerary'])
        
        user = users_collection.find_one({'_id': ObjectId(req['user_id'])})
        
        if user['role'] == 'driver':
            list_req['od'].append(req)
        elif user['role'] == 'passenger':
            list_req['op'].append(req)
        elif user['role'] == 'mainly_driver':
            list_req['md'].append(req)
        elif user['role'] == 'mainly_passenger':
            list_req['mp'].append(req)
            
    return list_req

# Convert Itinerary dict to List
def convert_itinerary_dict_to_list(itin:dict) -> list:
    """
        index 0 : origin
        |itin| - 1 : destination
        1..|itin| - 2 : vias
    """
    itinerary = []
    
    itinerary.append(itin['origin'])
    if len(itin['vias']):
        for via in itin['vias']:
            if(via == None): continue
            itinerary.append(via)
    itinerary.append(itin['destination'])
    
    print("================> Itinerary")
    print(itinerary)
    
    return itinerary

# get location index from all locations
def get_location_index(coord) -> int:
    global all_locations
        
    for index, loc in enumerate(all_locations):
        if loc['id'] == generate_unique_id(coord):
            return index
        
# Get data from origin-destination matrix
def get_duration_from_matrix(matrix, coord_1, coord_2):
    index_1 = get_location_index(coord_1)
    index_2 = get_location_index(coord_2)
        
    return timedelta(minutes=matrix[index_1][index_2]['duration'])

# Add a solution to the solutions list
def add_solution(req):
    solutions.append({'id': req['id'], 'available_seats': req['available_seats'], 'itinerary' : req['itinerary']})
    
# Insert (or not) a position into an itinerary
def insert_position_into_itinerary(matrix, position:dict, sol_itin:list, available_seats:int, inserted_index:int=0) -> tuple():
    can_be_inserted = False
    
    for sol_itin_index in range(inserted_index, len(sol_itin)-1):
        """
            i = current location
            j = next location
            k = location to insert
        """
        # Constraint of time window
        """print("==========================================> ")
        print(sol_itin_index)
        print("==========================================> ")
        print(position)"""
        
        hour_1 = stringToDateTime(sol_itin[sol_itin_index]['hour_at_least']) + get_duration_from_matrix(matrix, sol_itin[sol_itin_index]['coordinates'], position['coordinates'])
        hour_2 = hour_1 + get_duration_from_matrix(matrix, position['coordinates'], sol_itin[sol_itin_index+1]['coordinates'])
        
        # If the duration from i to k is not between window [hk-, hk+]
        #print(hour_1 > stringToDateTime(position['hour_at_last']))
        if hour_1 > stringToDateTime(position['hour_at_last']):
            continue
        
        # If the duration from i to k + k to j is not between window [hj-, hj+]
        #print(hour_2 > stringToDateTime(sol_itin[sol_itin_index+1]['hour_at_last']))
        if hour_2 > stringToDateTime(sol_itin[sol_itin_index+1]['hour_at_last']):
            continue
        
        # Available seats constraint
        difference_i = sol_itin[sol_itin_index]['number_of_pickups'] -  sol_itin[sol_itin_index]['number_of_drop_offs']
        difference_k = position['number_of_pickups'] -  position['number_of_drop_offs']
        difference_j = sol_itin[sol_itin_index + 1]['number_of_pickups'] -  sol_itin[sol_itin_index + 1]['number_of_drop_offs']
        
        if difference_i + difference_k > available_seats:
            continue
        
        if difference_i + difference_k + difference_j > available_seats:
            continue
        
        # Propagation of capacity throught all following positions

        
        # All constrainst are verified so insert the position
        can_be_inserted = True
        sol_itin.insert(sol_itin_index+1, position)
        inserted_index = sol_itin_index+1
        break
   
    return can_be_inserted, sol_itin, inserted_index

# Insert (or not) a request into the solutions
def insert_itinerary_into_solutions(matrix, req) -> bool:  
    if len(solutions) == 0 : return False
    
    inserted = False
        
    for sol_index in range(len(solutions)):
        req_itin = req['itinerary']
        sol_itin = solutions[sol_index]['itinerary']
        
        # Check if the request is between the origin hour and destination hour of the current solution
        # Constraint of time window        
        if stringToDateTime(req_itin[0]['hour_at_last']) <  stringToDateTime(sol_itin[0]['hour_at_least']) or stringToDateTime(req_itin[len(req_itin)-1]['hour_at_least']) >  stringToDateTime(sol_itin[len(sol_itin)-1]['hour_at_last']) :
            # Skip the current itinerary solution
            continue
            
        # Try to insert all positions (origin, vias, desitnation) into the current solution itinerary
        inserted_index = 0
        
        for position in req_itin:            
            # inserted_index to know the index the index of the previous position inserted (0 by default)
            inserted, sol_itin, inserted_index =  insert_position_into_itinerary(matrix, position, sol_itin, solutions[sol_index]['available_seats'], inserted_index)
            
            # If the current position is not inserted, break the loop of positions and go to the next solution
            if not inserted:
                break
            
        if inserted:
            solutions[sol_index]['itinerary'] = sol_itin
            break
    
    return inserted
    
# Greedy matching algorithm
def greedy_algo(matrix) -> list:
    #Extract all Requests
    extract_requests()
    
    """ 
        Step 1 : Loop over the whole OnlyDriver List (L_OD)
                 Insert the itinerary of every item of this list into the solution
  
        Step 2 : Loop over the whole OnlyPassenger List (L_OP)
                 For every item, loop over the whole Solutions List
                 Verify if the OnlyPassenger demand can be inserted to the current item of solution (according to some constraints)
                    if yes, insert
                 If the OnlyPassenger demand doesn't find a solution, keep it
                 
        Step 3 : Do the step 2 by replacing the OnlyPassenger Demand by MainlyPassenger Demand
        
        Step 4 : Do the step 2 by replacing the OnlyPassenger Demand by MainlyDriver Demand
                 For those MainlyDriver demands that didn't find solution,
                 Add them the Solutions List itself

        At this step we have all OnlyDriver demands that are itinerary in the solutions list,
                             some OnlyPassenger demands that are inside an itinerary of the solutions list and the rest no
                             some MainlyPassenger demands that are inside an itinerary of the solutions list and the rest no
                             some OnlyPassenger demands that are inside an itinerary and the rest as itinerary of the solutions list
                             
        Step 5 : Restart from step 2 to step 3 in order to find an itinerary as solution for remaining OnlyPassenger and MainPassenger
        
        If it remains some MainlyPassenger demands
        
        Step 6 : Add them as itinerary to the solutions list and reparse for finding itinerary for the remaining OnlyPassenger demands
                 
        Important : As the project is multi objectives, we decide to maximize the number of request to satisfy 
                    instead of reduce number of vehicles in traffic that is why we start by OnlyPassenger & MainlyPassenger instead of mainlyDriver
        
        Constraints : Hour of location (origin, destination, vias) and number of available seats
                             
    """
    
    # Step 1
    if (len(list_req['od'])):
        for req in list_req['od']:
            add_solution(req)
            list_req['od'].remove(req)
    
        # Step 2
        if (len(list_req['op'])):
            for req in list_req['op']:
                if insert_itinerary_into_solutions(matrix, req) :
                    list_req['op'].remove(req)                  
            
        # Step 3
        if (len(list_req['mp'])):
            for req in list_req['mp']:
                if insert_itinerary_into_solutions(matrix, req) :
                    list_req['mp'].remove(req)
            
        # Step 4
        if (len(list_req['md'])):
            for req in list_req['md']:
                if insert_itinerary_into_solutions(matrix, req) :
                    list_req['md'].remove(req)

    if (len(list_req['md'])):
        for req in list_req['md']:
            add_solution(req)
            list_req['md'].remove(req)
            
    # Step 5
        # Step 2
    if (len(list_req['op'])):
        for req in list_req['op']:
            if insert_itinerary_into_solutions(matrix, req) :
                list_req['op'].remove(req)
            
        # Step 3
    for req in list_req['mp']:
        if insert_itinerary_into_solutions(matrix, req) :
            list_req['mp'].remove(req)
    
    # Step 6
    if (len(list_req['mp'])):
        for req in list_req['mp']:
            add_solution(req)
            list_req['mp'].remove(req)
    
    if (len(list_req['op'])):
        for req in list_req['op']:
            if insert_itinerary_into_solutions(matrix, req) :
                list_req['op'].remove(req)
    
    # Result 
    #return solutions

# Computation of the whole process
def computation():
    # Remove the excel file
    """if os.path.exists('origin-destination_matrix.xlsx'):
        os.remove('origin-destination_matrix.xlsx')"""
        
    global all_locations
        
    # Extract and preprocess locations
    all_locations = extract_locations()
    all_locations = add_ids_to_locations(all_locations)
    all_locations = filter_unique_locations(all_locations)
    
    print_locations(all_locations)

    # Compute the orign-destination matrix
    # matrix = build_matrix(all_locations)
    
    # For testing
    matrix = [
        [{'duration': 0},  {'duration': 4}, {'duration':   4}, {'duration':  16}, {'duration': 4.5}, {'duration':  16}],
        [{'duration': 4},  {'duration': 0}, {'duration':  15}, {'duration':   2}, {'duration':  14}, {'duration':   2}],
        [{'duration': 4},  {'duration': 15}, {'duration':   0}, {'duration':  12}, {'duration': 0.5}, {'duration':  12}],
        [{'duration': 16}, {'duration': 2}, {'duration':  12}, {'duration':   0}, {'duration':  12}, {'duration': 0.5}],
        [{'duration': 4.5},{'duration': 14}, {'duration': 0.5}, {'duration':  12}, {'duration':   0}, {'duration': 0.5}],
        [{'duration': 16}, {'duration': 2}, {'duration':  12}, {'duration': 0.5}, {'duration': 0.5}, {'duration':   0}],
    ]
                
    # Execute greedy matching algorithm
    greedy_algo(matrix)
    
    return solutions
