import streamlit as st 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Database connection
engine = create_engine('mysql+pymysql://root:Abcd1234@127.0.0.1:3306/redbus')

# Function to fetch data
@st.cache_data
def fetch_data(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# Fetch initial data
initial_query = "SELECT * FROM bus_routes"
initial_data = fetch_data(initial_query)

# Handle NaN and missing data
initial_data['duration'] = initial_data['duration'].str.extract(r'(\d+)').astype(float).fillna(0).astype(int)

# Title and Filters
st.title(":red[RedBus Application]")

st.markdown("### Filter by Bus Type and Route")
col1, col2 = st.columns(2)

with col1:
    
    st.write("Filter by State:")
    state_filter = st.multiselect(
        "Select State(s):",
        options=np.append(['Anything'], initial_data['states'].unique()),
        key="state_filter"  # unique key for this filter
    )       

with col2:
    # Update Route Filter based on selected States
    st.write("Filter by State Routes:")
    if state_filter and 'Anything' not in state_filter:
        available_routes = initial_data[initial_data['states'].isin(state_filter)]['route_name'].unique()
    else:
        available_routes = initial_data['route_name'].unique()

    route_filter = st.multiselect(
        "Select Route:",
        options=np.append(['Anything'], available_routes),
        key="route_filter"  # unique key for this filter
    )

# Sidebar Filters
with st.sidebar:
    st.header(":red[Additional Filters]")
    
    # Price Range Filter
    st.write("Select Price Range:")
    price_options = ['Anything', '0-250', '250-500', '500-1000', '1000-1500', '1500+']
    selected_price = st.radio(
        "Price Range",
        options=price_options,
        index=0,
        key="price_filter"  # unique key for this filter
    )
    price_filter_map = {
        'Anything': (initial_data['price'].min(), initial_data['price'].max()),
        '0-250': (0, 250),
        '250-500': (250, 500),
        '500-1000': (500, 1000),
        '1000-1500': (1000, 1500),
        '1500+': (1500, initial_data['price'].max())
    }
    price_filter = price_filter_map[selected_price]

    bustype_filter = st.multiselect(
        "Select Bus Type:",
        options=np.append(['Anything'], initial_data['bustype'].unique()),        
        key="bustype_filter"  # unique key for this filter
    )

    # Star Rating Filter
    star_rating_filter = st.slider(
        "Star Rating",
        min_value=1.0,
        max_value=5.0,
        value=(1.0, 5.0),
        step=0.1,
        key="star_rating_filter"  # unique key for this filter
    )

    # Seat Availability Filter
    availability_filter = st.selectbox(
        "Minimum Seat Availability:",
        options=['Anything'] + [str(i) for i in range(0, int(initial_data['seats_available'].max()) + 1)],
        index=0,
        key="availability_filter"  # unique key for this filter
    )
    availability_filter = None if availability_filter == 'Anything' else int(availability_filter)

    # Time Filters (Departure & Arrival)
    time_options = ['Anything', '0-6', '6-12', '12-18', '18-24']
    selected_departure = st.radio(
        "Departure Time Range",
        options=time_options,
        index=0,
        key="departure_time_filter"  # unique key for this filter
    )
    selected_arrival = st.radio(
        "Arrival Time Range",
        options=time_options,
        index=0,
        key="arrival_time_filter"  # unique key for this filter
    )
    time_map = {
        'Anything': (0, 24),
        '0-6': (0, 6),
        '6-12': (6, 12),
        '12-18': (12, 18),
        '18-24': (18, 24)
    }
    departure_filter = time_map[selected_departure]
    arrival_filter = time_map[selected_arrival]

    # Duration Filter
    selected_duration = st.radio(
        "Duration Range (hours)",
        options=['Anything', '0-2', '2-4', '4-6', '6+'],
        index=0,
        key="duration_filter"  # unique key for this filter
    )
    duration_map = {
        'Anything': (0, initial_data['duration'].max()),
        '0-2': (0, 2),
        '2-4': (2, 4),
        '4-6': (4, 6),
        '6+': (6, initial_data['duration'].max())
    }
    duration_filter = duration_map[selected_duration]

# Query construction
query = "SELECT * FROM bus_routes WHERE 1=1"

if bustype_filter and 'Anything' not in bustype_filter:
    query += f" AND bustype IN ({','.join([f'\"{b}\"' for b in bustype_filter])})"

if route_filter and 'Anything' not in route_filter:
    query += f" AND route_name IN ({','.join([f'\"{r}\"' for r in route_filter])})"

# Apply filtering for states correctly
if state_filter and 'Anything' not in state_filter:
    state_conditions = ','.join([f'\"{s.strip().lower()}\"' for s in state_filter])
    query += f" AND LOWER(TRIM(states)) IN ({state_conditions})"

query += f" AND price BETWEEN {price_filter[0]} AND {price_filter[1]}"

if availability_filter is not None:
    query += f" AND seats_available >= {availability_filter}"

query += f" AND star_rating BETWEEN {star_rating_filter[0]} AND {star_rating_filter[1]}"
query += f" AND HOUR(departing_time) BETWEEN {departure_filter[0]} AND {departure_filter[1]}"
query += f" AND HOUR(reaching_time) BETWEEN {arrival_filter[0]} AND {arrival_filter[1]}"
query += f" AND duration BETWEEN {duration_filter[0]} AND {duration_filter[1]}"

# Fetch filtered data
filtered_data = fetch_data(query)

# Display results
st.markdown("### Filtered Output")
st.dataframe(filtered_data)

# Download button
if not filtered_data.empty:
    st.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.warning("No data available with the selected filters.")
