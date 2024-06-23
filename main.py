from dataclasses import dataclass
import sys
import csv
import random
from math import radians, sin, cos, atan2, sqrt

COORDINATES_FILE = 'dane1.csv'
KM_earth_R = 6371