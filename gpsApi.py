import serial
import pynmea2
from typing import Optional, Tuple
import math
from geopy.distance import geodesic

def connect_gps(port: str = 'COM9', baudrate: int = 9600) -> Optional[serial.Serial]:
    """Подключение к GPS устройству"""
    try:
        gps = serial.Serial(port, baudrate, timeout=1)
        #GPSdata=gps.read()
        print(f"Успешное подключение к {port}")
        return gps
    except serial.SerialException as e:
        print(f"Ошибка подключения: {e}")
        return None

def get_coords(gps: serial.Serial) -> Optional[Tuple[float, float]]:
    """Получение валидных координат с проверкой фикса"""
    while True:
        try:
            line = gps.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$GPGGA'):
                data = pynmea2.parse(line)
                
                # Проверка качества фикса (0=нет, 1=GPS, 2=DGPS)
                if data.gps_qual in (1, 2) and data.latitude != 0 and data.longitude != 0:
                    return (data.latitude, data.longitude)
                else:
                    print("Ожидание GPS фикса...")
                    
        except UnicodeDecodeError:
            print("Ошибка декодирования строки")
        except pynmea2.ParseError:
            print("Ошибка разбора NMEA")
        except Exception as e:
            print(f"Ошибка: {e}")
            return None
        



def get_navigation_data(current_pos, target_pos, max_speed=0.5, max_angular=1.0):
    """
    Вычисляет расстояние до цели, линейную и угловую скорость.
    
    Args:
        current_pos: tuple (широта, долгота) - текущие координаты
        target_pos: tuple (широта, долгота) - координаты цели
        max_speed: float - макс. линейная скорость (м/с)
        max_angular: float - макс. угловая скорость (рад/с)
    
    Returns:
        dict: {
            'distance': расстояние до цели (м),
            'linear_speed': линейная скорость (м/с),
            'angular_speed': угловая скорость (рад/с),
            'direction': текстовое описание направления
        }
    """
    # Расчет расстояния
    distance = geodesic(current_pos, target_pos).meters
    
    # Расчет угла к цели
    lat1, lon1 = math.radians(current_pos[0]), math.radians(current_pos[1])
    lat2, lon2 = math.radians(target_pos[0]), math.radians(target_pos[1])
    dlon = lon2 - lon1
    
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    angle = math.atan2(x, y)
    
    # Нормализация угла (-π до π)
    angle = (angle + math.pi) % (2 * math.pi) - math.pi
    
    # Расчет скоростей
    linear_speed = min(distance * 0.3, max_speed)  # Коэффициент 0.3 можно настраивать
    angular_speed = max(-max_angular, min(angle * 0.5, max_angular))  # Коэффициент 0.5
    
    # Определение направления
    degrees = math.degrees(angle)
    if -45 <= degrees < 45:
        direction = "вперёд"
    elif 45 <= degrees < 135:
        direction = "налево"
    elif -135 <= degrees < -45:
        direction = "направо"
    else:
        direction = "разворот"
    
    return {
        'distance': round(distance, 2),
        'linear_speed': max(0, round(linear_speed, 2)),  # Только положительная
        'angular_speed': round(angular_speed, 2),
        'direction': direction
    }