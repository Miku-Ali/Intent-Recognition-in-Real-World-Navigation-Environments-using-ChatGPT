import json
import googlemaps
from datetime import datetime
import math
import re
from openai import OpenAI
import os
import requests



def geocode_points(points_list):

    geocoded_points = []
    for item in points_list:
        if isinstance(item, list):
            # Recursive call for nested lists
            geocoded_points.append(geocode_points(item))
        else:
            # Geocode the item
            geocode_result = gmaps.geocode(item)
            if geocode_result:
                # Assuming the first result is the most relevant
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']
                geocoded_points.append((lat, lng))
            else:
                # Handle cases where no result is found
                print(f"No geocode result for: {item}")
                geocoded_points.append(None)
    return geocoded_points





def get_route_google(origin, destination):

    # Request directions
    now = datetime.now()
    route = []
    for i in range(len(origin)):
        tem_route = []
        for j in range(len(destination[i])):
            tem_route_2 = []
            directions_result = gmaps.directions(origin[i],
                                                destination[i][j],
                                                mode="driving",
                                                departure_time=now)
  
            tem_route_2.append(origin[i])

            for leg in directions_result[0]['legs']:
                for step in leg['steps']:
                    coord_1 = (step['start_location']['lat'], step['start_location']['lng'])
                    coord_2= (step['end_location']['lat'], step['end_location']['lng'])
                    
                    if coord_1 not in tem_route_2:
                        tem_route_2.append(coord_1)
                        
                    if coord_2 not in tem_route_2:
                        tem_route_2.append(coord_2)

        
            for k in range (len(obs[i])):
                if obs[i][k] in tem_route_2:
                    print("yes")

            tem_route_2.append(destination[i][j])
            tem_route.append(tem_route_2)
            

        route.append(tem_route)

    return route



def get_route_googole_waypoints(origin, destination,obs):

    
    # Request directions
    now = datetime.now()
    route = []
    for i in range(len(origin)):
        tem_route = []
        
        for j in range(len(destination[i])):
            tem_route_2 = []
            directions_result = gmaps.directions(origin[i],
                                                destination[i][j],
                                                mode="driving",
                                                waypoints=obs[i],
                                                departure_time=now)
            
            tem_route_2.append(origin[i])
                            
            for leg in directions_result[0]['legs']:
                for step in leg['steps']:
                    coord_1 = (step['start_location']['lat'], step['start_location']['lng'])
                    coord_2= (step['end_location']['lat'], step['end_location']['lng'])
                    
                    if coord_1 not in tem_route_2:
                        tem_route_2.append(coord_1)
                        
                    if coord_2 not in tem_route_2:
                        tem_route_2.append(coord_2)

            tem_route_2.append(destination[i][j])
            tem_route.append(tem_route_2)

        route.append(tem_route)

    return route



def get_route_ai(origin, destination):

    pattern = re.compile(r'\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)')
    
    routes = []  
    
    for i in range(len(origin)):

        route_per_origin = []
        
        for j in range(len(destination[i])):

  

            response = client.chat.completions.create(
                model = "gpt-3.5-turbo-0125",  
                messages=[
                    {"role": "system", "content": "You only need to provide latitude, longitude of key locations. Don't provide anything else than lat and lng in the format (latitude,longitude)"},
                    {"role": "user", "content": f"Provide the shortest  with {len(obs[i])+5} key locations path between {origin[i]} and {destination[i][j]} by car"},
                ]
            )
            responses = response.choices[0].message.content
            
            list_1 = [list(map(float, pattern.match(coord).groups())) for coord in responses.split('\n') if pattern.match(coord)]

            list_1.insert(0,list(origin[i]))
            list_1.append(list(destination[i][j]))
            route_per_origin.append(list_1)

          
        
        routes.append(route_per_origin)
    
    return routes


def get_route_ai_waypoints(origin, destination,obs):

    pattern = re.compile(r'\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)')
    
    routes = []  
    
    for i in range(len(origin)):

        route_per_origin = []

        for j in range(len(destination[i])):
                

                response = client.chat.completions.create(
                    model = "gpt-3.5-turbo-0125",  
                    messages=[
                        {"role": "system", "content": "You only need to provide latitude, longitude of key locations. Don't provide anything else than lat and lng in the format (latitude,longitude)"},
                        {"role": "user", "content": f"Provide the shortest with{obs[i]} and other {len(obs[i])+5} key locaionts path between {origin[i]} and {destination[i][j]} by car"},
                    ]
                )
                responses = response.choices[0].message.content
                list_1 = [list(map(float, pattern.match(coord).groups())) for coord in responses.split('\n') if pattern.match(coord)]

                list_1.insert(0,list(origin[i]))

                list_1.append(list(destination[i][j]))

                route_per_origin.append(list_1)


        
        routes.append(route_per_origin)
    
    return routes


def get_route_ai_no_waypoints(origin, destination,obs):

    pattern = re.compile(r'\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)')
    
    routes = []  
    
    for i in range(len(origin)):

        route_per_origin = []
        

        for j in range(len(destination[i])):
                

                response = client.chat.completions.create(
                    model = "gpt-3.5-turbo-0125",  
                    messages=[
                        {"role": "system", "content": "You only need to provide latitude, longitude of key locations. Don't provide anything else than lat and lng in the format (latitude,longitude)"},
                        {"role": "user", "content": f"Provide the shortest with {len(obs[i])+5} key locaionts and do not via {obs[i]} path between {origin[i]} and {destination[i][j]} by car"},
                    ]
                )
                responses = response.choices[0].message.content
                
                
                list_1 = [list(map(float, pattern.match(coord).groups())) for coord in responses.split('\n') if pattern.match(coord)]

                list_1.insert(0,list(origin[i]))

                list_1.append(list(destination[i][j]))
                
                route_per_origin.append(list_1)


        routes.append(route_per_origin)
    
    return routes





def get_routes_mapbox(init,goals,access_token):

    mapbox_waypoints = []

    for i in range(len(init)):

        tem = []

        for j in range(len(goals[i])):

            tem_1 = [list(init[i])] 
            
            tem_1.append(list(goals[i][j]))  
            
            tem.append(tem_1) 

        mapbox_waypoints.append(tem)



    all_routes_coordinates = []

    for route_list in mapbox_waypoints:
        tem = []
        for waypoints in route_list:
            waypoints_str = ';'.join([f"{lon},{lat}" for lat, lon in waypoints])
            
            url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{waypoints_str}?geometries=geojson&access_token={access_token}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                coordinates = data['routes'][0]['geometry']['coordinates']
                route_coordinates = [(lat, lon) for lon, lat in coordinates]
                tem.append(route_coordinates)
            else:
                tem.append(f"Error: API request unsuccessful. Status code: {response.status_code}")
                continue

        all_routes_coordinates.append(tem)

    return all_routes_coordinates






def get_routes_mapbox_obs(init,goals,obs, access_token):

    mapbox_waypoints = []

    for i in range(len(init)):

        tem = []

        for j in range(len(goals[i])):

            tem_1 = [list(init[i])] 
            
            for obs_point in obs[i]:

                tem_1.append(obs_point)
            
            tem_1.append(list(goals[i][j]))  
            
            tem.append(tem_1) 

        mapbox_waypoints.append(tem)


    all_routes_coordinates = []

    for route_list in mapbox_waypoints:
        tem = []
        for waypoints in route_list:
            waypoints_str = ';'.join([f"{lon},{lat}" for lat, lon in waypoints])
            
            url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{waypoints_str}?geometries=geojson&access_token={access_token}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                coordinates = data['routes'][0]['geometry']['coordinates']
                route_coordinates = [(lat, lon) for lon, lat in coordinates]
                tem.append(route_coordinates)
            else:
                tem.append(f"Error: API request unsuccessful. Status code: {response.status_code}")
                continue

        all_routes_coordinates.append(tem)

    return all_routes_coordinates




#calculate distance between two points 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance



# distance between init and goals
def cal_cost_dif_google(route_google):

    distances = []

    for i in range(len(route_google)):

        tem_dis = []

        for j in range(len(route_google[i])):
                       
            distance  = 0 

            for  k in range(len(route_google[i][j])-1):
            
                distance += haversine(route_google[i][j][k][0], route_google[i][j][k][1], route_google[i][j][k+1][0], route_google[i][j][k+1][1])

            tem_dis.append(distance)

        distances.append(tem_dis)

        
        
    return distances


#calculate difference between obs and un-obs 
def cal_cost_dif_google_obs(route_google_obs):


    distances = []

    for i in range(len(route_google_obs)):

        tem_dis = []

        for j in range(len(route_google_obs[i])):
                       
            distance  = 0 

            for  k in range(len(route_google_obs[i][j])-1):
            
                distance += haversine(route_google_obs[i][j][k][0], route_google_obs[i][j][k][1], route_google_obs[i][j][k+1][0], route_google_obs[i][j][k+1][1])

            tem_dis.append(distance)

        distances.append(tem_dis)

        
        
    return distances



#calculate cost difference for ai 

def cal_cost_dif_ai(route_ai):


    distances = []

    for i in range(len(route_ai)):

        tem_dis = []

        for j in range(len(route_ai[i])):
                       
            distance  = 0 

            # print("tem_dis before ",tem_dis)

            for  k in range(len(route_ai[i][j])-1):
            
                distance += haversine(route_ai[i][j][k][0], route_ai[i][j][k][1], route_ai[i][j][k+1][0], route_ai[i][j][k+1][1])
                # print("distance",distance)

            tem_dis.append(distance)
            # print("tem_dis after ",tem_dis)

        distances.append(tem_dis)
        # print("distances total", distances)

        
        
    return distances



def cal_cost_dif_ai_obs(route_ai_obs):

    distances = []

    for i in range(len(route_ai_obs)):

        tem_dis = []

        for j in range(len(route_ai_obs[i])):
                       
            distance  = 0 

            for  k in range(len(route_ai_obs[i][j])-1):

                distance += haversine(route_ai_obs[i][j][k][0], route_ai_obs[i][j][k][1], route_ai_obs[i][j][k+1][0], route_ai_obs[i][j][k+1][1])
            
            tem_dis.append(distance)

        distances.append(tem_dis)

    return distances



def cal_cost_dif_ai_no_obs(route_ai_no_obs):

    distances = []

    for i in range(len(route_ai_no_obs)):

        tem_dis = []

        for j in range(len(route_ai_no_obs[i])):
                       
            distance  = 0 

            for  k in range(len(route_ai_no_obs[i][j])-1):
            
                distance += haversine(route_ai_no_obs[i][j][k][0], route_ai_no_obs[i][j][k][1], route_ai_no_obs[i][j][k+1][0], route_ai_no_obs[i][j][k+1][1])

            tem_dis.append(distance)

        distances.append(tem_dis)

    return distances




def cal_cost_mapbox(route_mapbox):

    distances = []

    for i in range(len(route_mapbox)):

        tem_dis = []

        for j in range(len(route_mapbox[i])):
                       
            distance  = 0 

            for  k in range(len(route_mapbox[i][j])-1):
            
                distance += haversine(route_mapbox[i][j][k][0], route_mapbox[i][j][k][1], route_mapbox[i][j][k+1][0], route_mapbox[i][j][k+1][1])

            tem_dis.append(distance)

        distances.append(tem_dis)

    return distances





def cal_cost_mapbox_obs(route_mapbox):

    distances = []

    for i in range(len(route_mapbox)):

        tem_dis = []

        for j in range(len(route_mapbox[i])):
                       
            distance  = 0 

            for  k in range(len(route_mapbox[i][j])-1):
            
                distance += haversine(route_mapbox[i][j][k][0], route_mapbox[i][j][k][1], route_mapbox[i][j][k+1][0], route_mapbox[i][j][k+1][1])

            tem_dis.append(distance)

        distances.append(tem_dis)

    return distances



#final probaility calculation
def cal_probility_google(cost_dif_google,cost_dif_google_obs):

    prob = []
    cost = []

    # calculate the cost difference between path with obs and path without obs
    for i in range(len(cost_dif_google)):

        total_cost = 0
        tem_cost   = []

        for j   in range(len(cost_dif_google[i])):

            total_cost = cost_dif_google[i][j] - cost_dif_google_obs[i][j]
            tem_cost.append(total_cost)
        
        cost.append(tem_cost)


    for i in range (len(cost)):
        
        tem_prob = []

        for j in range(len(cost[i])):

            probility = (alpha * math.exp((-beta)*(cost[i][j])))/( 1+ math.exp((-beta)*(cost[i][j])))

            tem_prob.append(probility)

        prob.append(tem_prob)

    return  prob


def cal_probility_ai_obs(cost_dif_ai_obs,cost_dif_ai_no_obs):

    prob = []
    cost = []

    # calculate the cost difference between path with obs and path without obs
    for i in range(len(cost_dif_ai_obs)):

        total_cost = 0
        tem_cost   = []

        for j   in range(len(cost_dif_ai_obs[i])):

            total_cost = cost_dif_ai_obs[i][j] - cost_dif_ai_no_obs[i][j]
            tem_cost.append(total_cost)
        
        cost.append(tem_cost)


    for i in range (len(cost)):
        
        tem_prob = []

        for j in range(len(cost[i])):

            probility = (alpha * math.exp((-beta)*(cost[i][j])))/( 1+ math.exp((-beta)*(cost[i][j])))

            tem_prob.append(probility)

        prob.append(tem_prob)

    return  prob


def cal_probility_ai_simpler(cost_dif_ai_obs,cost_dif_ai):

    prob = []
    cost = []

    # calculate the cost difference between path with obs and path without obs
    for i in range(len(cost_dif_ai_obs)):

        total_cost = 0
        tem_cost   = []

        for j   in range(len(cost_dif_ai_obs[i])):

            total_cost = cost_dif_ai_obs[i][j] - cost_dif_ai[i][j]
            tem_cost.append(total_cost)
        
        cost.append(tem_cost)


    for i in range (len(cost)):
        
        tem_prob = []

        for j in range(len(cost[i])):

            probility = (alpha * math.exp((-beta)*(cost[i][j])))/( 1+ math.exp((-beta)*(cost[i][j])))

            tem_prob.append(probility)

        prob.append(tem_prob)

    return  prob



def cal_probility_mapbox(cost_dif_mapbox,cost_dif_mapbox_obs):

    prob = []
    cost = []

    # calculate the cost difference between path with obs and path without obs
    for i in range(len(cost_dif_mapbox)):

        total_cost = 0
        tem_cost   = []

        for j   in range(len(cost_dif_mapbox[i])):

            total_cost = cost_dif_mapbox[i][j] - cost_dif_mapbox_obs[i][j]
            tem_cost.append(total_cost)
        
        cost.append(tem_cost)


    for i in range (len(cost)):
        
        tem_prob = []

        for j in range(len(cost[i])):

            probility = (alpha * math.exp((-beta)*(cost[i][j])))/( 1+ math.exp((-beta)*(cost[i][j])))

            tem_prob.append(probility)

        prob.append(tem_prob)

    return  prob




def coor_accuracy(goal,goals,probility):

    ans = len(goal)

    rigth_ans = 0


    for i in range(len(probility)):

        value = max(probility[i])

        position = probility[i].index(value)

        print("goal :",goal[i])
        print("goals :",goals[i][position] )

        if  goal[i] == goals[i][position]:

            rigth_ans += 1

        else:
            rigth_ans +=0
    
    accuracy =  rigth_ans/ans

    return accuracy 



            

# read data
file_path = "./goals_data.json"
with open(file_path, 'r') as file:
    data = json.load(file)


#init data
init_point  = [entry['initial'] for entry in data]

init_goal   = [entry['intent_goal'] for entry in data]

init_goals  = [entry['goals'] for entry in data]

obs         = [entry['observations'] for entry in data]


#Load Google Api
api_key = 'AIzaSyCFfNMPGWRnN8OF5fvnPa_ZnChdvjwqOXc'
gmaps = googlemaps.Client(api_key)


#Load openai Api 
api_key =  "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"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))

#load mapbox api 
access_token = 'pk.eyJ1IjoibWlrdTE2IiwiYSI6ImNsdHFvbGVvdTA5dWEya252eXJ2aGx0cHAifQ.uY4n9Nhzj9mCsOudsReeXA'


# before calculate this probility, make sure u changed the list of positions to list of longtitude and latitude of postions 
alpha = 10
beta = 1


# Change all points to their longitude and latitude
init  = geocode_points(init_point[:2])


goal = geocode_points(init_goal[:2])


goals = geocode_points(init_goals[:2])


obs_test = obs[:2]



#get  the routes 
route_google =  get_route_google(init,goals)

route_google_obs = get_route_googole_waypoints(init,goals,obs_test)

route_ai = get_route_ai(init,goals)

route_ai_obs  = get_route_ai_waypoints(init,goals,obs_test)

route_ai_no_obs = get_route_ai_no_waypoints(init,goals,obs_test)

routes_mapbox = get_routes_mapbox(init, goals,access_token)

routes_mapbox_obs = get_routes_mapbox_obs(init,goals,obs, access_token)




#calculate the cost difference 
cost_dif_google  = cal_cost_dif_google(route_google)

cost_dif_google_obs = cal_cost_dif_google_obs(route_google_obs)

cost_dif_ai = cal_cost_dif_ai(route_ai)

cost_dif_ai_obs = cal_cost_dif_ai_obs(route_ai_obs)

cost_dif_ai_no_obs = cal_cost_dif_ai_no_obs(route_ai_no_obs)

cost_dif_mapbox = cal_cost_mapbox(routes_mapbox)

cost_dif_mapbox_obs = cal_cost_mapbox_obs(routes_mapbox_obs)




#probility of each fomula 
probility_google = cal_probility_google(cost_dif_google,cost_dif_google_obs)

probility_google_simpler = cal_probility_google(cost_dif_google,cost_dif_google_obs)

probility_ai  = cal_probility_ai_obs(cost_dif_ai_obs,cost_dif_ai_no_obs)
# print("probility_ai",probility_ai)

probility_ai_simpler = cal_probility_ai_simpler(cost_dif_ai_obs,cost_dif_ai)
# print("probility_ai_simpler",probility_ai_simpler)

probility_mapbox = cal_cost_mapbox(cost_dif_mapbox,cost_dif_mapbox_obs)

probility_mapbox_simpler = cal_cost_mapbox(cost_dif_mapbox,cost_dif_mapbox_obs)


#similarity
google_accuracy = coor_accuracy(goal,goals,probility_google)
# print("google_accurcy",google_accurcy)

google_simpler_accuracy = coor_accuracy(goal,goals,probility_google_simpler)
# print("google_simpler_accuracy",google_simpler_accuracy)


ai_accuracy = coor_accuracy(goal,goals,probility_ai)

# print("ai_accuracy",ai_accuracy)

ai_simpler_accuracy = coor_accuracy(goal,goals,probility_ai_simpler)

# print("ai_simpler_accuracy",ai_simpler_accuracy)

mapbox_accuracy = coor_accuracy(goal,goals,probility_mapbox)

mapbox_simpler_accuracy = coor_accuracy(goal,goals,probility_mapbox_simpler)




