import streamlit as st
from db_helper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox(
    'Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2 = st.columns(2)
    cities = db.fetch_city_names()
    with col1:
        source = st.selectbox('Source', sorted(cities))
    with col2:
        destination = st.selectbox('Destination', sorted(cities))

    if st.button("Search"):
        results = db.fetch_all_flights(source, destination)
        st.dataframe(results)

elif user_option == 'Analytics':
    st.title('Analytics')

    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        )
    )

    st.header('Total flights')
    st.plotly_chart(fig)

    city, frequency1 = db.busy_airport()
    fig2 = px.bar(
        x=city,
        y=frequency1
    )
    st.header('Busiest City')
    st.plotly_chart(fig2)

    date, frequency2 = db.daily_frequency()
    fig3 = px.line(
        x=date,
        y=frequency2
    )
    st.header('Daily Frequency of Flights')
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.title('Tell about the project')
