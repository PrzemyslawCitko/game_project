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