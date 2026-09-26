import folium
import geopandas as gpd
import os
import glob

# Paths to shapefiles
base_path = r"d:\Dam break Work\Dam Break CCCSS\data\processed"
shapefiles = {
    "Basin": os.path.join(base_path, "BasinSHP", "Dehrang_DBA_Basin.shp"),
    "Damwall": os.path.join(base_path, "Damwall", "Damwall.shp"),
    "River Centerline": os.path.join(base_path, "RIver line & Buffer", "Rivercentreline .shp"),
    "River Buffer 50m": os.path.join(base_path, "RIver line & Buffer", "Riverline_Buffer_50m.shp"),
    "Reservoir Submergence": os.path.join(base_path, "Submergence", "Reservoir_Submergence_Dehrang.shp")
}

# Create a folium map centered roughly on Panvel / Dehrang Dam area
# We will get the bounds from the first valid shapefile
m = None

colors = {
    "Basin": "blue",
    "Damwall": "red",
    "River Centerline": "cyan",
    "River Buffer 50m": "green",
    "Reservoir Submergence": "purple"
}

for name, path in shapefiles.items():
    if os.path.exists(path):
        try:
            gdf = gpd.read_file(path)
            # Ensure it's in lat/lon format (EPSG:4326)
            if gdf.crs and gdf.crs.to_string() != "EPSG:4326":
                gdf = gdf.to_crs(epsg=4326)
            elif not gdf.crs:
                gdf.set_crs(epsg=4326, inplace=True)
                
            if m is None:
                # Initialize map on first dataset
                bounds = gdf.total_bounds
                center_lat = (bounds[1] + bounds[3]) / 2
                center_lon = (bounds[0] + bounds[2]) / 2
                m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
            
            # Add to map
            folium.GeoJson(
                gdf,
                name=name,
                style_function=lambda x, color=colors[name]: {
                    'color': color,
                    'weight': 2,
                    'fillOpacity': 0.3
                }
            ).add_to(m)
        except Exception as e:
            print(f"Error processing {name}: {e}")

if m:
    folium.LayerControl().add_to(m)
    m.save(r"d:\Dam break Work\Dam Break CCCSS\docs\map_overview.html")
    print("Map generated successfully.")
else:
    print("No map generated.")
