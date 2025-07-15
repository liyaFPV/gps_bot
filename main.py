from gpsApi import *

gps_device = connect_gps('COM10') 
target = (56.1005245, 54.2337052)
while True:
    #print(gps_device.readline())
    latitude, longitude = get_coords(gps_device)
    print(f"Координаты: {latitude:.6f}, {longitude:.6f}")
    current=(latitude,longitude)

    data = get_navigation_data(current, target)
    print(f"До цели: {data['distance']} м")
    print(f"Скорость: {data['linear_speed']} м/с")
    print(f"Поворот: {data['angular_speed']} рад/с ({data['direction']})")
    print(f"Рекомендация: Двигаться {data['direction']} со скоростью {data['linear_speed']} м/с")