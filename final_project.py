'''
Name: Jiayang Xu
Class: CS230 Section4
Data: US Stadiums geocoded
URL:
Description: This program will use Streamlit and its features to show virtualize the stadium distribution as long as its relative statistical results.
             Including the sorted original data, sort data by your own perameter, relavent charts, and location map.

THANK YOU AND HAVE A NICE SUMMER!
'''



import pandas as pd
import streamlit as st
import plotly as px
import pydeck as pdk
#The package plotly is a package that we did not use in class.

# Load dataset
path = '/Users/jasonxu/Desktop/PythonProject/final project/stadiums-geocoded.csv'
df = pd.read_csv(path)

def get_stadiums_by_conference(df, conference='All'):
    if conference != 'All':
        return df[df['conference'] == conference]
    else:
        return df

def get_max_capacity_stadium(df, conference='All'):
    conf_df = get_stadiums_by_conference(df, conference)
    max_cap = conf_df['capacity'].max()
    stadium_df = conf_df[conf_df['capacity'] == max_cap]
    return stadium_df, max_cap

def filter_stadiums_by_year(df, year_range):
    return df[(df['built'] >= year_range[0]) & (df['built'] <= year_range[1])]

# Set font style and alignment for title (This is amazing. I used different size and color to make it more readable and virtualized)
title_html = "<h1 style='font-family: Arial, sans-serif; color: #ff5733; text-align: center;'>Stadium Analysis</h1>"
st.markdown(title_html, unsafe_allow_html=True)
st.write()

sub1 = "<h1 style='font-family: Arial, sans-serif; color: #ff5733; text-align: left; font-size:25px'>At a Glance</h1>"
st.markdown(sub1, unsafe_allow_html=True)
st.dataframe(df)

# Sidebar
st.sidebar.title('Parameters')
conferences = df['conference'].unique().tolist()
conference_select = st.sidebar.selectbox('Select a Conference', ['All'] + conferences)
# Sidebar 1
st.subheader(f'Maximum Capacity Stadium in {conference_select} Conference')
stadium, max_cap = get_max_capacity_stadium(df, conference_select)
st.dataframe(stadium)
st.write(f'The maximum capacity is {max_cap}.')

# Sidebar 2
year_range = st.sidebar.slider('Year Range for Stadium Construction', int(df['built'].min()), int(df['built'].max()), (1950, 2023))
filtered_stadiums = filter_stadiums_by_year(df, year_range)
st.subheader(f'Stadiums Built Between {year_range[0]} and {year_range[1]}')
st.dataframe(filtered_stadiums)

# Sidebar 3
state_input = st.sidebar.text_input('Enter State Name').upper()
if state_input:
    st.subheader(f'Stadiums in {state_input}')
    state_stadiums = df[df['state'] == state_input]
    st.dataframe(state_stadiums)
    st.write(f'There are {len(state_stadiums)} stadiums in {state_input}.')

# Sidebars above is amazing. This took me much time. We can drag the year range to what you want, and the subheader will change along with the time frame.

# Sidebar 4
st.sidebar.header('Special Filtering')
selected_conferences = st.sidebar.multiselect('Select Conferences', ['All'] + conferences)
capacity_min = st.sidebar.slider('Minimum Capacity', int(df['capacity'].min()), int(df['capacity'].max()), int(df['capacity'].min()))
capacity_max = st.sidebar.slider('Maximum Capacity', capacity_min, int(df['capacity'].max()), int(df['capacity'].max()))

filtered_df = df.copy()
if 'All' not in selected_conferences:
    filtered_df = filtered_df[filtered_df['conference'].isin(selected_conferences)]
filtered_df = filtered_df[(filtered_df['capacity'] >= capacity_min) & (filtered_df['capacity'] <= capacity_max)]

sub2 = "<h1 style='font-family: Arial, sans-serif; color: #ff5733; text-align: left; font-size:25px'>Special Filtering</h1>"
st.markdown(sub2, unsafe_allow_html=True)
st.dataframe(filtered_df)

# Charts Title
sub3 = "<h1 style='font-family: Arial, sans-serif; color: #ff5733; text-align: left; font-size:25px'>Supporting Charts</h1>"
st.markdown(sub3, unsafe_allow_html=True)

# Histogram of stadium capacities
fig1 = px.histogram(df, x="capacity", nbins=50, title="Distribution of Stadium Capacities")
fig1.update_traces(marker_color= '#ADD8E6')  # Customize the color
fig1.update_layout(
    xaxis_title='Capacity',
    yaxis_title='Count'
)
st.plotly_chart(fig1)

# Pie chart of stadiums by state
st.write()
st.write()
fig2 = px.pie(df, names='div',title='Percentage of Stadiums in Each Division')
fig2.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=1
    ),
    height=800,
    width=700
)
st.plotly_chart(fig2)

# Bar Chart for Capacity and Conference
fig = px.bar(df, x='conference', y='capacity', color='conference', title='Stadium Capacity by Conference')
st.plotly_chart(fig)


# Map
sub4 = "<h1 style='font-family: Arial, sans-serif; color: #ff5733; text-align: left; font-size:25px'>Where are They</h1>"
st.markdown(sub4, unsafe_allow_html=True)

df['icon_data'] = [{"url": "https://img.icons8.com/plasticine/100/000000/marker.png", "width": 50, "height": 50, "anchorY": 128} for _ in range(len(df))]
df['expanded'] = df['expanded'].replace({pd.np.nan: 'Unknown'})
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

#Initial View
initial_view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=4,
    pitch=0)

# Layer
layer = pdk.Layer(
    type='IconLayer',
    data=df,
    get_icon='icon_data',
    get_size=4,
    size_scale=5,
    get_position=['longitude', 'latitude'],
    pickable=True
)
map_ = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=initial_view_state,
    layers=[layer],
    tooltip={
        'html': '<b>Stadium:</b> {team}<br/><b>City:</b> {city}<br/><b>State:</b> {state}<br/><b>Conference:</b> {conference}',
        'style': {
            'backgroundColor': 'steelblue',
            'color': 'white'
        }
    }
)
st.pydeck_chart(map_)
