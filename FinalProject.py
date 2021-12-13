"""
Class: CS230
Name: Esther Krystek
Date: 12/13/2021
Program Name: Final Project - Skyscrapers
Description: Data Visualization Project with Dataset of Skyscrapers and their Information
"""

#Imports
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

#Filename
FNAME = "Skyscrapers2021.csv"

#Read data from csv file into Pandas dataframe
def get_data():
    return pd.read_csv(FNAME)

#Create a table to display all the data
#The user can filter the data by selecting several parameters
def filter_table(df):
    columns = ['CITY', 'MATERIAL', 'FUNCTION']
    for column in columns:
        options = pd.Series((df[column]).unique())
        choice = st.multiselect("Select {}.".format(column.lower()), options)
        if choice != []:
            df = df[df[column].isin(choice)]
    choose = ['No', 'Yes']
    page1 = st.radio('Choose completion date', choose)
    page2 = st.radio('Choose number of floors', choose)
    columns2 = ['COMPLETION', 'FLOORS']
    if page1 == 'Yes':
        options = pd.Series((df[columns2[0]]).unique())
        options.sort_values(ascending = True)
        choice = st.select_slider("Select {}.".format(columns2[0].lower()), options)
        if choice != []:
            df = df[df[columns2[0]] == choice]
    if page2 == 'Yes':
        options = pd.Series((df[columns2[1]]).unique())
        options.sort_values(ascending = True)
        choice = st.select_slider("Select {}.".format(columns2[1].lower()), options)
        if choice != []:
            df = df[df[columns2[1]] == choice]
    return df

#Display the locations of the skyscapers on a map with the name, city and a link as information
def map(df):
    map = folium.Map(location=[40.693943, -73.985880], default_zoom_start=15)
    for index, row in df.iterrows():
        name = row['NAME'] + ', ' + row['CITY'] + ', ' + row['Link']
        folium.Marker(
            location = [row['latitude'], row['longitude']],
            popup = name,
            tooltip = "Click for more"
        ).add_to(map)
    folium_static(map)
    return df

#Display a graph that shows the evolvements of heights of the skyscapers over the time they were completed
def evolvement_over_time(df):
    df_new = df.drop(['RANK','NAME','CITY','Full Address','latitude','longitude','Height','Feet','FLOORS','MATERIAL','FUNCTION','Link'], axis=1)
    df_new['Meters'] = df_new['Meters'].str.replace('m', '')
    df_new['Meters'] = pd.to_numeric(df_new['Meters'])
    df_mean = df_new.groupby(['COMPLETION'])[['Meters']].mean().reset_index()
    df_mean['COMPLETION'] = pd.to_numeric(df_mean['COMPLETION'])
    df_mean = df_mean.set_index("COMPLETION")
    page_names = ["Bar chart", "Line chart"]
    page = st.radio('Format', page_names)
    if page == "Bar chart":
        st.bar_chart(df_mean)
    else:
        st.line_chart(df_mean)
    mean = df_new['Meters'].mean()
    st.write("The mean value is ", mean)

#Display a graph that shows the five top cities in terms of quantities of skyscrapers and their heights
def top_cities(df):
    df_new = df.drop(['RANK','NAME','Full Address','latitude','longitude','COMPLETION','Height','Feet','FLOORS','MATERIAL','FUNCTION','Link'], axis=1)
    df_new['Meters'] = df_new['Meters'].str.replace('m', '')
    df_new['Meters'] = pd.to_numeric(df_new['Meters'])
    df_sum = df_new.groupby(['CITY'])[['Meters']].sum().reset_index()
    df_sum = df_sum.set_index('CITY')
    st.bar_chart(df_sum['Meters'].nlargest(n=5))

#Show the percentages of materials that were used to build the skyscrapers in a pie chart
def percentages_materials(df):
    df.insert(0, 'Number', 1)
    df_new = df.groupby(['MATERIAL'])[['Number']].sum().reset_index()
    fig = go.Figure(
        go.Pie(
        labels = df_new['MATERIAL'],
        values = df_new['Number'],
        hoverinfo = "label+percent",
        textinfo = "value"
    ))
    st.plotly_chart(fig)

#Show the percentages of functions of the skyscrapers in a pie chart
def percentages_functions(df):
    df_new = df.groupby(['FUNCTION'])[['Number']].sum().reset_index()
    fig = go.Figure(
        go.Pie(
        labels = df_new['FUNCTION'],
        values = df_new['Number'],
        hoverinfo = "label+percent",
        textinfo = "value"
    ))
    st.plotly_chart(fig)

def main():
    from PIL import Image
    img = Image.open("skyscrapers.jpg")
    st.image(img, width=500)
    st.title("Welcome to my Final Project")
    df = get_data()
    st.header("Filter Data")
    st.write(filter_table(df))
    st.header("Display On Map")
    df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
    map(df)
    st.header("Evolvements of Heights Over Time")
    evolvement_over_time(df)
    st.header("The Five Top Cities")
    top_cities(df)
    st.header("Percentages of Materials")
    percentages_materials(df)
    st.header("Percentages of Functions")
    percentages_functions(df)

main()
