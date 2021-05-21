# https://github.com/asehmi/Data-Science-Meetup-Oxford/blob/master/GlobalCities/app.py

import pandas as pd
import streamlit as st
import pydeck as pdk

st.sidebar.header('About')
st.sidebar.info('Tamil Nadu Hospitals Corona Bed Status. The data is sourced from https://stopcorona.tn.gov.in/beds.php \n\n' + \
    'Contact: http://sol-ai.in/\n')

df = pd.read_csv("tn_covid_district_beds.csv")
df_hospital = pd.read_csv("tn_covid_beds.csv")

data_columns = ['District','latitude','longitude','COVID BEDS_Vacant']

data = df[data_columns]
data['Value'] = data['COVID BEDS_Vacant']

districts = data['District'].unique()
selected_district = st.sidebar.selectbox("Select a District to see Hospital level beds", districts)
st.sidebar.markdown("---")

COLOUR_RANGE = [
    [0,240,0,220],
    [0,200,0,220],
    [0,160,0,220],
    [0,130,0,220],
    [0,100,0,220],
]
TEXT_COLOUR = {
    'Black': [0,0,0,255],
    'Red': [189,27,33,255],
    'Green': [0,121,63,255],
    'Gold': [210,160,30,255]
}

radius_scale=1.0
opacity=0.8
text_colour = TEXT_COLOUR.get('Black')
radius_unit = 500000.0 # in metres

st.sidebar.write("Settings")
radius_scale = st.sidebar.slider('Bubble size', min_value=0.1, max_value=2.0, step=0.1, value=1.0)
opacity = st.sidebar.slider('Bubble opacity', min_value=0.1, max_value=1.0, step=0.05, value=0.8)
text_colour = TEXT_COLOUR.get( st.sidebar.selectbox('Text colour', list(TEXT_COLOUR.keys())) )

max = data.loc[:,'Value'].max(axis=0)
min = data.loc[:,'Value'].min(axis=0)
data.loc[:,'normValue'] = ((data.loc[:,'Value'] / (max - min))*radius_unit*radius_scale)

# calculate colour range mapping index to then assign fill colour
data.loc[:,'fillColorIndex'] = ( (data.loc[:,'Value']-min) / (max-min) )*(len(COLOUR_RANGE) - 1)
data.loc[:,'fill_color'] = data.loc[:,'fillColorIndex'].map(lambda x: COLOUR_RANGE[int(x)])


st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=11,
        longitude=77.5,
        zoom=6.1,
        pitch=0
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
             data=data,
             pickable=True,
             get_position='[longitude, latitude]',
             get_color='[200, 30, 0, 160]',
             get_radius='normValue',
             radius_min_pixels=2*radius_scale,
             radius_max_pixels=30*radius_scale,
             get_fill_color='fill_color',
             get_line_color=[128,128,128,200],
             get_line_width=4000,
             stroked=True,
             filled=True,
             opacity=opacity),
        pdk.Layer(
            type='TextLayer',
            id='text-layer',
            data=data,
            pickable=True,
            get_position=['longitude', 'latitude'],
            get_text='District',
            get_color=text_colour,
            billboard=False,
            get_size=11,
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor='"middle"',
            get_alignment_baseline='"center"'
            )
        ],
        tooltip = {"html": "{District}<br/>Available:{Value}"}
    )
)

if selected_district:
    st.subheader(f"Beds in {selected_district} District:")
    hosp_data = df_hospital[df_hospital['District'] == selected_district]
    st.write(hosp_data)
