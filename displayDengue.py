#create venv, then proceed to install require library in the venv for dependencies
#pip install streamlit folium pandas geopandas pydeck
#pip install --upgrade pip

import streamlit as st
import pandas as pd
import geopandas as gpd

# Function to upload CSV and load DataFrame
def load_data(file):
    df = pd.read_csv(file)
    return df

# Function to convert DataFrame to GeoDataFrame
def create_geo_dataframe(df):
    geometry = gpd.points_from_xy(df['long'], df['lat'])
    gdf = gpd.GeoDataFrame(df, crs='EPSG:4326', geometry=geometry)
    return gdf

# Main Streamlit app
def main():
    st.title('Spatial Data Visualization with Filters')

    # Upload CSV file
    uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        gdf = create_geo_dataframe(df)

        # Rename the columns to match Streamlit's expectations
        gdf = gdf.rename(columns={'lat': 'LATITUDE', 'long': 'LONGITUDE'})

        # Display the main map with point data
        st.subheader('Main Map')
        st.map(gdf)

        # Sidebar filters
        st.sidebar.title('Filters')
        selected_gender = st.sidebar.multiselect('Select Gender', df['gender'].unique())
        selected_category = st.sidebar.multiselect('Select Category', df['category'].unique())
        selected_distance = st.sidebar.slider('Select Distance', float(df['distance'].min()), float(df['distance'].max()), (float(df['distance'].min()), float(df['distance'].max())))
        selected_age = st.sidebar.slider('Select Age', int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
        selected_city = st.sidebar.multiselect('Select City', df['city'].unique())
        selected_day = st.sidebar.selectbox('Select Day', df['day'].unique())

        # Filter data based on selected filters
        filtered_gdf = gdf[
            (gdf['gender'].isin(selected_gender)) &
            (gdf['category'].isin(selected_category)) &
            (gdf['distance'].between(selected_distance[0], selected_distance[1])) &
            (gdf['age'].between(selected_age[0], selected_age[1])) &
            (gdf['city'].isin(selected_city)) &
            (gdf['day'] == selected_day)
        ]

        # Display the filtered data
        st.write('Filtered Data:')
        st.write(filtered_gdf)

        # Button to refresh the map based on filtered data
        if st.button('Refresh Map'):
            st.subheader('Filtered Map')
            st.map(filtered_gdf)

# Run the Streamlit app
if __name__ == '__main__':
    main()
