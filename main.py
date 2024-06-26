from dataclasses import dataclass
import sys
import csv
import random
from math import radians, sin, cos, atan2, sqrt
from typing import List, Optional

COORDINATES_FILE = 'dane1.csv'
KM_earth_R = 6371

@dataclass
class Coordinate:
    """
    Represents coordinates of the country's capital
    
    Atributes:
        lon (float): Longitude of the capital.
        lat (float): Latitude of the capital.
    """
    country: str
    capital: str
    lon: float
    lat: float

@dataclass
class Distance:
    """
    Represents distance betwween two capitals
    
    Atributes:
    actual_country (str): Drawn/chosen country
    actual_capital (str): Drawn/chosen capital
    another_country (str): Second country 
    another_capital (str): Second capital 
    distance (float): Distance between drawn/chosen capital and second capital in km
    """
    actual_country: str
    actual_capital: str
    another_country: str
    another_capital: str
    distance: float


def load_coordinates() -> List[Coordinate]:
    """
    Load countries, capitals and coordinates from csv file
    
    Returns list of Coordinate objects containing coordinates of the capitals
    """
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


def draw_capital(coordinates: List[Coordinate]) -> Coordinate:
    """
    Draw country/capital from Coordinate list
    """
    drawn_capital = random.choice(coordinates)
    return drawn_capital


def create_distance_between_capitals(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Count distance between two coordiantes in km
        """
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


def create_distances(drawn_capital: Coordinate, coordinates: List[Coordinate], exclude_countries: Optional[List[str]]=None) -> List[Distance]:
    """
    Create list of distances between drawn/chosen capital and another capitals
    """
    if exclude_countries is None:
        exclude_countries = []
    list_of_distances = []
    for coordinate in coordinates: 
        if coordinate.country in exclude_countries:
            continue
        distances = Distance(
            actual_country=drawn_capital.country,
            actual_capital=drawn_capital.capital,
            another_country=coordinate.country,
            another_capital=coordinate.capital,
            distance=create_distance_between_capitals(
                drawn_capital.lon, drawn_capital.lat, coordinate.lon, coordinate.lat
            ),
        )
        if distances.distance != 0: 
            list_of_distances.append(distances)
    return list_of_distances


def find_closest_capital(distances: List[Distance]) -> Distance:
    """
    Finds the closest capital from the distance list
    """
    return min(distances, key=lambda d: d.distance)


def main():
    coordinates = load_coordinates()
    drawn_capital = draw_capital(coordinates)
    print(drawn_capital)
    distances = create_distances(drawn_capital, coordinates)
    closest = find_closest_capital(distances)
    exclude_countries = [drawn_capital.country]

    while distances:
        country = input()
        if country == closest.another_country:
            print('OK')
            exclude_countries.append(country)
            print(exclude_countries)
            next_country = next((c for c in coordinates if c.country == closest.another_country), None)
            if next_country:
                distances = create_distances(next_country, coordinates, exclude_countries)
                print(distances)
                if not distances:
                    print('You won!')
                    break
                closest = find_closest_capital(distances)
                print(closest)
        else:
            print('Wrong answer.')
            break


if __name__ == "__main__":
    main()