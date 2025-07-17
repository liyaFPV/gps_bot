from gpsApi import *
import json
from colorama import *
import time

fail="data.json"
gps_data=y = json.dumps(fail)
gps_device = connect_gps('COM10') 
target = (56.1005245, 54.2337052)
while True:
    print(gps_device)
    time.sleep(1)
    """
    #latitude, longitude = get_coords(gps_device)
    latitude = 56.1005260
    longitude = 54.2337065
    print(f"Координаты: {latitude:.6f}, {longitude:.6f}")
    current=(latitude,longitude)
    data = get_navigation_data(current, target)
    if(data['distance'] <=0.3):
        print(Fore.GREEN+"\n цель достигнута")
        
    print(Fore.RESET)
    print(f"До цели: {data['distance']} м")
    print(f"Скорость: {data['linear_speed']} м/с")
    print(f"Поворот: {data['angular_speed']} рад/с ({data['direction']})")
    print(f"Рекомендация: Двигаться {data['direction']} со скоростью {data['linear_speed']} м/с")
    time.sleep(1)
    """