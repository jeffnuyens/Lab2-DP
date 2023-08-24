import streamlit as st
import pandas as pd 
import numpy as np 

data = pd.read_csv('tienda.csv', encoding= 'latin1')
city_data = pd.read_csv('states.csv')

st.title('Lab 2: Streamlit')

# Filtro de fecha utilizando order date y 4 filtros adicionale
st.sidebar.header('Filters')
selected_dates = st.sidebar.multiselect('Select Order Dates', data['Order_Date'].unique())
selected_ship_modes = st.sidebar.multiselect('Select Ship Modes', data['Ship_Mode'].unique())
selected_segments = st.sidebar.multiselect('Select Segments', data['Segment'].unique())
selected_states = st.sidebar.multiselect('Select States', data['State'].unique())
selected_categories = st.sidebar.multiselect('Select Categories', data['Category'].unique())

filtered_data = data[
    (data['Order_Date'].isin(selected_dates)) &
    (data['Ship_Mode'].isin(selected_ship_modes)) &
    (data['Segment'].isin(selected_segments)) &
    (data['State'].isin(selected_states)) &
    (data['Category'].isin(selected_categories))
]

# Tabla que resuma las ventas y cantidades, descuentos y profit 
summary_table = filtered_data.groupby(['Category', 'Sub-Category']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Discount': 'sum'
}).reset_index()

st.subheader('Summary Table')
st.write(summary_table)

# Resumen de estadísticas
st.subheader('Summary Statistics')
total_sales = summary_table['Sales'].sum()
total_quantity = summary_table['Quantity'].sum()
total_discount = filtered_data['Discount'].sum()
total_profit = filtered_data['Profit'].sum()

st.write('Total Sales:', total_sales)
st.write('Total Quantity:', total_quantity)
st.write('Total Discount:', total_discount)
st.write('Total Profit:', total_profit)

# Tabla de datos sin filtros
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(filtered_data)

# Gráficas de ventas por Estado
st.subheader('Sales by State')
ventas_por_estado = data.groupby("State")['Sales'].sum()

st.bar_chart(ventas_por_estado, use_container_width=True)

# Mapa con la data de ventas y por ciudad
st.subheader('Sales by City')
merged_data = data.merge(city_data, on=['City', 'State'], how='left')
map_data = merged_data.groupby(['lat', 'lon', 'City', 'State']).agg({'Sales': 'sum'}).reset_index()

st.map(map_data[['lat', 'lon', 'Sales']], use_container_width=True)
