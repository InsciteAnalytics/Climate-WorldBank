import pandas as pd
import numpy as np
import geopandas as gpd
import pandas as pd
import panel as pn
import holoviews as hv
import geoviews as gv
import geoviews.feature as gf
import cartopy
import cartopy.feature as cf
from bokeh.models import HoverTool
import hvplot.pandas
from geoviews import opts
from cartopy import crs as ccrs
gv.extension('bokeh')

# Loading countrywise temperature change data from local file
Train=pd.read_csv('tdiff4.csv')

# Loading countries shape file as geopandas Df
shapefile1='ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'
gdf1 = gpd.read_file(shapefile1)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf1.columns = ['country', 'country_code', 'geometry']
gdf1.drop(gdf1.index[159],inplace=True)

# Loading sovereignty shape file as geopandas Df
shapefile='ne_10m_admin_0_sovereignty/ne_10m_admin_0_sovereignty.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']
gdf.drop(gdf.index[163],inplace=True)
gdf.reset_index().drop('index',axis=1,inplace=True)

# Sao Tome & Principe had strange characters in its name that had to be fixed
gdf.replace(to_replace=gdf.country.loc[188],value='Sao Tome and Principe',inplace=True)

# Adding geometry of some missing countries from shapefile1 above
newcntlist=['Greenland','Kazakhstan','New Caledonia','Puerto Rico']
for i in newcntlist:
    missing=gdf1.loc[gdf1.country==i]
    gdf=pd.concat([gdf,missing])

# Forming final Df for using in plot
geodf=pd.merge(gdf,Train,on='country')

# Making the plot and using panel for embedding to enable later use (saved plot as html file named 'tp')
tooltips = [
    ('Country', '@country'),
    ('ΔTemp(1901-2012)', '@tempchange')
]
hover = HoverTool(tooltips=tooltips)

templot=gv.Polygons(geodf,vdims=['tempchange','country']).opts(width=1000,height=600,colorbar=True,color_index='tempchange',tools=[hover])

pn.panel(templot).save('tp',embed=True)
