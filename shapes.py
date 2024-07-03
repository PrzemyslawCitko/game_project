# countries/ne_10m_admin_0_countries.shp
import folium.features
import geopandas as gpd
import folium
import json


SHAPE_FILE = "countries/ne_10m_admin_0_countries.shp"

world = gpd.read_file(SHAPE_FILE)

world.to_file('static/world.geojson', driver='GeoJSON', encoding='utf-8')

with open('static/world.geojson', 'r', encoding='utf-8') as reader:
    geojson_data = json.load(reader)

m = folium.Map(location=[0, 80], zoom_start=2)

geo_json = folium.GeoJson(geojson_data, name='Borders').add_to(m)

geo_json.add_child(folium.features.GeoJsonTooltip(fields=['ADMIN'], labels=False))

map_file = 'templates/map.html'
m.save(map_file)