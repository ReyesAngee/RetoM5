import pandas as pd
from pathlib import Path
import streamlit as st
from PIL import Image
import altair as alt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Files neede to load the web app are inside an asset folder in te root project
assets = Path('')
df_path = assets / 'kpis.csv'
logo = assets / 'logo.jpg'

# load DF of employees with only the needed columns
employee_df = pd.read_csv(df_path, usecols = [
    'id_employee', 'absences',
    'name_employee','birth_date', 'age',
    'gender','marital_status', 'hiring_date',
    'position','salary', 'performance_score',
    'last_performance_date','average_work_hours', 'satisfaction_level',
])
employee_df.set_index('id_employee', inplace=True)
employee_df['gender'] = employee_df['gender'].apply(lambda x: x.strip())

st. set_page_config(layout="wide")

# sidebar with filters
with st.sidebar:
    st.title('Filtros')

    # Radio button with gender options
    gender_option = st.radio('GÃ©nero', employee_df['gender'].dropna().unique())

    # Slider with performance score
    performance_serie = employee_df['performance_score'].dropna().unique()
    performance_serie.sort()
    performance_range = st.select_slider(
        'Rango de desempeÃ±o',
        options=performance_serie,
        value=(performance_serie[0], performance_serie[-1])
    )

    # dropdown to select marital status of employee
    selected_status = st.selectbox("Estatus civil", employee_df['marital_status'].dropna().unique())

# Header with image, title and text description
image = Image.open(logo)


st.image(image=image, use_column_width='auto')
st.title('AnÃ¡lisis de desempeÃ±o')
st.text('Dashboard de desempeÃ±o de colaboradores de Socialize your knowledge')
#st.divider()

performance_employee_filter = employee_df.loc[
    (employee_df['performance_score'] >= performance_range[0]) & (employee_df['performance_score'] <= performance_range[-1]) if isinstance(performance_range, tuple) and len(performance_range) > 1
    else (employee_df['performance_score'] == performance_range),
    :
]

with st.container():
    employees_size = employee_df.groupby('gender')['gender'].count()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header(employees_size.sum())
        st.subheader("Empleados")
   
    with col2:
        st.header(employees_size['F'])
        st.subheader("Mujeres")

    with col3:
        st.header(employees_size['M'])
        st.subheader("Hombres")

# st.divider()
col1, col2 = st.columns(2)

with col1:
    with st.container():
        # container to show/hide histogram graph of performance filtered by performance slider, gender radio button
        performance_plot = alt.Chart(
            performance_employee_filter,
            title="DesempeÃ±o por gÃ©nero"
        ).mark_bar(
            interpolate='step',
            color='pink' if (gender_option == 'F') else 'orange'
        ).encode(
            # x=alt.X('performance_score:N', bin=False).axis(labelAngle=0).title('Desempeno'),
            # y=alt.Y('count(performance_score):Q', stack=None).axis().title('Num de empleados'),
        ).transform_filter(
            alt.FieldEqualPredicate(field='gender', equal=gender_option)
        ).transform_filter(alt.FieldEqualPredicate(field='marital_status', equal=selected_status))


        st.altair_chart(performance_plot, use_container_width=True)


        # container to show/hide plot of avg work hours vs age
        salary_col = 'salary'
        age_area_df = performance_employee_filter.groupby('age').agg({salary_col: ['mean', 'min', 'max']})
        x = age_area_df.index.to_list()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=age_area_df[salary_col].loc[:, 'min'],
            showlegend=False,
            name='min',
            fill=None,
            mode='lines',
            line=dict(color='rgba(255, 0, 0, 0.0)'),
        ))
        fig.add_trace(go.Scatter(
            showlegend=False,
            name='max',
            x=x,
            y=age_area_df[salary_col].loc[:, 'max'],
            fill='tonexty',
            mode='none',
            fillcolor='rgba(75, 0, 130, 0.12)',
        ))
        fig.add_trace(go.Scatter(
            name='AVG',
            x=x,
            y=age_area_df[salary_col].loc[:, 'mean'],
            line=dict(color='rgba(75, 0, 130, 0.86)', width=2, dash='dash'),
        ))
        # update labels
        fig.update_layout(
            yaxis_tickprefix = '$',
            xaxis_title="Edad",
            yaxis_title="Salario",
            title='Salario por edad',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container():
        # container to show/hide plot of mean hours by gender
        mean_hour_scatter = alt.Chart(
            employee_df,
            title="Horas promedio por gÃ©nero"
        ).mark_boxplot(
            extent="min-max",
            size=50
        ).encode(
            #x=alt.X('gender:O').axis(labelExpr=("datum.label == 'F' ? 'Mujer' : 'Hombre'"), labelAngle=0).title('GÃ©nero'),
            #y=alt.Y("average_work_hours:Q").scale(zero=False).title('Horas promedio'),
           
            color=alt.Color('gender', legend=None)
        )
        st.altair_chart(mean_hour_scatter, use_container_width=True)


        # container to show/hide plot of avg work hours vs performance
        performance_area_df = performance_employee_filter.groupby('performance_score').agg({'average_work_hours': ['mean', 'min', 'max']})
        x = performance_area_df.index.to_list()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=performance_area_df['average_work_hours'].loc[:, 'min'],
            showlegend=False,
            name='min',
            fill=None,
            mode='lines',
            line=dict(color='rgba(255, 0, 0, 0.0)'),
        ))
        fig.add_trace(go.Scatter(
            showlegend=False,
            name='max',
            x=x,
            y=performance_area_df['average_work_hours'].loc[:, 'max'],
            fill='tonexty',
            mode='none',
            fillcolor='rgba(75, 0, 130, 0.12)',
        ))
        fig.add_trace(go.Scatter(
            name='AVG',
            x=x,
            y=performance_area_df['average_work_hours'].loc[:, 'mean'],
            line=dict(color='rgba(75, 0, 130, 0.86)', width=2, dash='dash'),
        ))
        # update labels
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = x,
            ),
            xaxis_title="DesempeÃ±o",
            yaxis_title="Horas promedio al mes",
            title='Horas promedio por desempeÃ±o',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# conclusion
# st.divider()
st.header('ConclusiÃ³n')
st.text(r'''Las mujeres represetan la mayor fuerza laboral en la empresa con el 56% del total de empleados. Entre esto destaca que ambos gÃ©neros tienen un mayor desempeÃ±o en la categorÃ­a 3 entre 4 categooÃ­as pero las mujeres
tienen un trabajo de horas promedio mayor que el de los hombres, con una media de 4330hrs con respecto a 4230hrs de los hombres y en general un mayor grado de horas promedio al mes. En cuanto al salario por edad si
bien a los 42 y 67 aÃ±os hay un aumento considerable de salario solo a los 67 parace existir para la mayorÃ­a de estas personas, pues a los 42 aÃ±os hay un mÃ¡ximo salarial de $220K pero promedio solo de $78K,
posiblemente por el salario de los gerentes en comparaciÃ³n del de las posiciones mÃ¡s repetidas
''')