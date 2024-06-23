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