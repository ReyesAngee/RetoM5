import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px

DATA_URL = ('Employees.csv')

@st.cache
def load_data(nrows):
    Employees = pd.read_csv(DATA_URL, nrows=nrows)
    return Employees   

data_load_state = st.text('Loading data...')
Employees = load_data(500)
data_load_state.text('Done ! using cache...')

# Título de la aplicación
st.title('Análisis de Deserción de Empleados')


# Función para buscar empleados con cache
def buscar_empleados(Employee_ID, Hometown, Unit):
    resultados = Employees[(Employees['Employee_ID'] == Employee_ID) |
                      (Employees['Hometown'] == Hometown) |
                      (Employees['Unit'] == Unit)]
    return resultados

Employee_ID = st.text_input('Employee_ID', '')
Hometown = st.text_input('Hometown', '')
Unit = st.text_input('Unit', '')

if st.button('Buscar'):
    resultados = buscar_empleados(Employee_ID, Hometown, Unit)
    
    # Mostrar resultados encontrados
    st.subheader('Resultados Encontrados')
    st.dataframe(resultados)
    
    # Mostrar total de empleados encontrados
    total_encontrados = resultados.shape[0]
    st.write(f'Total de Empleados Encontrados: {total_encontrados}')

# Descripción de la búsqueda
st.write('Utiliza las cajas de texto y el botón de búsqueda para encontrar empleados por Employee_ID, Hometown o Unit.')




# Sidebar con checkbox
st.sidebar.header('Opciones')
show_dataframe = st.sidebar.checkbox('Mostrar DataFrame Completo', value=True)


# Contenido principal
st.header('Tabla de Datos')
if show_dataframe:
    st.dataframe(Employees)
else:
    st.write("Utiliza el checkbox para mostrar el DataFrame completo.")

    
# Sidebar con selectbox para el nivel educativo
st.sidebar.header('Filtrar por Nivel Educativo')
nivel_educativo_options = Employees['Education_Level'].unique()
selected_nivel_educativo = st.sidebar.selectbox('Selecciona un Nivel Educativo', nivel_educativo_options)

#######################################################################3
# Filtrar empleados por Nivel Educativo seleccionado
empleados_por_Education_Level = Employees[Employees['Education_Level'] == selected_nivel_educativo]

# Mostrar empleados por Nivel Educativo seleccionado en un dataframe
st.subheader(f'Empleados en {selected_nivel_educativo}')
st.dataframe(empleados_por_Education_Level)

# Mostrar total de empleados en Nivel Educativo seleccionado
total_empleados_Education_Level = empleados_por_Education_Level.shape[0]
st.write(f'Total de Empleados en {selected_nivel_educativo}: {total_empleados_Education_Level}')  

##########################################################
# Sidebar con selectbox para filtrar por Hometown
st.sidebar.header('Filtrar por Ciudad')
hometown_options = Employees['Hometown'].unique()
selected_hometown = st.sidebar.selectbox('Selecciona una Ciudad', hometown_options)

# Filtrar empleados por Hometown seleccionada
empleados_por_hometown = Employees[Employees['Hometown'] == selected_hometown]

# Mostrar empleados por Hometown en un dataframe
st.subheader(f'Empleados en {selected_hometown}')
st.dataframe(empleados_por_hometown)

# Mostrar total de empleados en Hometown seleccionada
total_empleados_hometown = empleados_por_hometown.shape[0]
st.write(f'Total de Empleados en {selected_hometown}: {total_empleados_hometown}')

#############################################################################

# Sidebar con selectbox para filtrar por Unit
st.sidebar.header('Filtrar por unidad funcional')
Unit_options = Employees['Unit'].unique()
selected_Unit = st.sidebar.selectbox('Selecciona una Unidad funcional ', Unit_options)

# Filtrar empleados por Unit seleccionada
empleados_por_Unit = Employees[Employees['Unit'] == selected_Unit]

# Mostrar empleados por Unit en un dataframe
st.subheader(f'Empleados en {selected_Unit}')
st.dataframe(empleados_por_Unit)

# Mostrar total de empleados en Unit seleccionada
total_empleados_Unit = empleados_por_Unit.shape[0]
st.write(f'Total de Empleados en {selected_Unit}: {total_empleados_Unit}')

#############################################################################

# Crear un histograma de empleados agrupados por edad
st.header('Histograma de Empleados por Edad')
fig = px.histogram(Employees, x='Age', nbins=20, title='Histograma de Edades de Empleados' )
st.plotly_chart(fig)

#############################################################################

# Crear una gráfica de frecuencias para las unidades funcionales (Unit)
st.header('Relación entre Tiempo de Servicio y Tasa de Deserción')
fig = px.scatter(Employees, x='Time_of_service', y='Attrition_rate', title='Relación entre Tiempo de Servicio y Tasa de Deserción',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig)

##############################################################################

# Calcular el índice de deserción por ciudad (Hometown)
desercion_por_ciudad = Employees.groupby('Hometown')['Attrition_rate'].mean().reset_index()

# Ordenar las ciudades por el índice de deserción de mayor a menor
desercion_por_ciudad = desercion_por_ciudad.sort_values(by='Attrition_rate', ascending=False)


# Crear una gráfica de barras para visualizar el índice de deserción por ciudad
st.header('Índice de Deserción por Ciudad')
fig = px.bar(desercion_por_ciudad, x='Hometown', y='Attrition_rate', title='Índice de Deserción por Ciudad')
fig.update_xaxes(categoryorder='total descending')  # Ordenar las ciudades de mayor a menor deserción
st.plotly_chart(fig)

##############################################################################
# Configurar la paleta de colores pastel de Seaborn
sns.set(style="whitegrid")
pastel_palette = sns.color_palette("pastel")
sns.color_palette("pastel",10)

###################################################################################

# Crear una gráfica para visualizar la relación entre la edad y la tasa de deserción
st.header('Relación entre Edad y Tasa de Deserción')
fig = px.scatter(Employees, x='Age', y='Attrition_rate', title='Relación entre Edad y Tasa de Deserción')
st.plotly_chart(fig)

####################################################################################




##############################################################################
# Cierre de la aplicación
st.write('¡Gracias por utilizar el dashboard de análisis de deserción de empleados!')



