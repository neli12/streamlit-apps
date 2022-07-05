import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import geopandas as gp
from pathlib import Path

area = Path(__file__).parents[0] / 'area_shp.shp'
dados = Path(__file__).parents[0] / 'dados.csv'


st.set_page_config(layout = 'wide')

st.title('Produtividade da cana-de açúcar (kg/ha) nos anos 2000 a 2020')

@st.cache
def load_data():
	sp_sugarcane_data = pd.read_csv(dados, encoding ='ISO-8859-1', sep = ';')
	return sp_sugarcane_data

def load_area():
	area = gp.read_file(area)
	return area
	
a,b = st.columns([5,8])

with a:
	st.write('''
		***Descrição***

		Olá! Seja bem vindo. Esta é uma plataforma desenvolvida para mostrar a variabilidade da produtividade da cana-de-açúcar ao longo dos últimos 21 anos, um projeto desenvolvido 
		como parte do MBA em Data Science and Analytics da Esalq USP. Aqui você irá encontrar a variabilidade e a predição da produtividade para o ano de 2021, além de outras informações relacionadas a clima, solo e temperatura.

		Para estimar a produtividade da cana-de açúcar para o ano de 2021, a análise de "dados em panel" será utilizada.

		Os dados de produtividade foram coletados do IBGE e os dados de solo, clima e temperatura, da plataforma Google Earth Engine.
		
		Em breve mais atualizações!

		Espero que você goste! :)

		''')


with b:
	area = load_area()

	m = folium.Map(location = [-21.9, -48.2], tiles = 'CartoDB positron',
		name = "Light Map", zoom_start = 6, attr = "My Data attribution")

	##sp_sugarcane = f"dados.csv"
	sp_sugarcane_data = load_data()

	yield_options = ['YIELD_2000', 'YIELD_2001', 'YIELD_2002', 'YIELD_2003',
	'YIELD_2004', 'YIELD_2005', 'YIELD_2006', 'YIELD_2007', 'YIELD_2008',
	'YIELD_2009', 'YIELD_2010', 'YIELD_2011', 'YIELD_2012', 'YIELD_2013',
	'YIELD_2014', 'YIELD_2015', 'YIELD_2016', 'YIELD_2017', 'YIELD_2018',
	'YIELD_2019', 'YIELD_2020']

	selected = st.selectbox('Select choice', yield_options)

	folium.Choropleth(
		geo_data = area,
		name = "choropleth",
		data = sp_sugarcane_data,
		columns = ["NM_MUN", selected],
		key_on = "feature.properties.NM_MUN",
		fill_color = "YlOrRd",
		fill_opacity = 0.7,
		line_opacity = .1,
		legend_name = selected).add_to(m)

##folium.features.GeoJson('area.geojson',
##	name = "Counties", 
##	popup = folium.features.GeoJsonPopup(field = ["NM_MUN"])).add_to(m)
##
	folium_static(m)
