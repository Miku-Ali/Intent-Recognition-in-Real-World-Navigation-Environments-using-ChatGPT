import requests

init = [(51.5073638, -0.1641135), (51.5073638, -0.1641135)]
goals = [[(51.4993695, -0.1272993), (51.5194133, -0.1269566)], [(51.4993695, -0.1272993), (51.5194133, -0.1269566)]]
obs = [[[51.5124121, -0.160508]], [[51.5145479, -0.1595106], [51.5163708, -0.148802], [51.5165964, -0.1475077]]]
access_token = 'pk.eyJ1IjoibWlrdTE2IiwiYSI6ImNsdHFvbGVvdTA5dWEya252eXJ2aGx0cHAifQ.uY4n9Nhzj9mCsOudsReeXA'




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

print(mapbox_waypoints)




