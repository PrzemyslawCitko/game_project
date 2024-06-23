from dataclasses import dataclass
import sys
import csv
import random
from math import radians, sin, cos, atan2, sqrt

COORDINATES_FILE = 'dane1.csv'
KM_earth_R = 6371

@dataclass
class Coordinate:
    country: str
    capital: str
    lon: float
    lat: float

@dataclass
class Distance:
    actual_country: str
    actual_capital: str
    closest_country: str
    closest_capital: str
    distance: float


def load_coordinates():
    coordinates = []
    try:
        with open(COORDINATES_FILE, encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                coordinate = Coordinate(
                    country=row['country'],
                    capital=row['capital'],
                    lon=float(row['lon']),
                    lat=float(row['lat']),
                )
                coordinates.append(coordinate)
    except FileNotFoundError:
        print('Nie znaleziono pliku.')
        sys.exit(1)
    return coordinates   


def draw_capital(coordinates):
    drawn_capital = random.choice(coordinates)
    return drawn_capital


def create_distance_between_capitals(lon1, lat1, lon2, lat2):
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        lon1 = radians(lon1)
        lon2 = radians(lon2)

        dist_lat = lat2 - lat1
        dist_lon = lon2 - lon1

        a = sin(dist_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        dist = c * KM_earth_R
        return dist


def create_distances(drawn_capital, coordinates):
    list_of_distances = []
    for coordinate in coordinates:    
        distances = Distance(
            actual_country=drawn_capital.country,
            actual_capital=drawn_capital.capital,
            closest_country=coordinate.country,
            closest_capital=coordinate.capital,
            distance=create_distance_between_capitals(
                drawn_capital.lon, drawn_capital.lat, coordinate.lon, coordinate.lat
            ),
        )
        if distances.distance != 0: 
            list_of_distances.append(distances)
    return list_of_distances

def find_closest_capital(distances):
    return min(distances, key=lambda d: d.distance)


def main():
    coordinates = load_coordinates()
    drawn_capital = draw_capital(coordinates)
    
    print(drawn_capital)
    distances = create_distances(drawn_capital, coordinates)
    print(distances)
    closest = find_closest_capital(distances)
    print(closest)

    exclude_countries = []

    while distances:
        country = input()
        if country == closest.closest_country:
            print('OK')
            exclude_countries.append(country)
            next_country = next((c for c in coordinates if c.country == closest.closest_country), None)
            if next_country:
                print(next_country)
                distances = create_distances(next_country, coordinates, exclude_countries)
                print(distances)
                closest = find_closest_capital(distances)
                print(closest)
        else:
            print('Wrong answer.')
            break


if __name__ == "__main__":
    main()