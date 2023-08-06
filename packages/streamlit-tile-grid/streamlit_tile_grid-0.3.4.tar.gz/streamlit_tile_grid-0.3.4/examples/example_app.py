# Example Implementation

from streamlit_tile_grid.TileRenderer import TileGrid
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def app():
    st.set_page_config(layout="wide")
    st.sidebar.title("Streamlit Tile Grid")
    # Define the number of tiles and grid size
    num_tiles = 4

    # Add some widgets to the sidebar
    st.sidebar.header("Settings")
    tile_color = st.sidebar.color_picker("Tile Color", value="#61dafb")
    text_color = st.sidebar.color_picker("Text Color", value="#000")
    tile_shadow = st.sidebar.color_picker("Tile Shadow", value="#4398af")
    num_tiles = st.sidebar.number_input("Number of Tiles", min_value=1, max_value=20, value=num_tiles)

    title_list = ['Customer Lost Minutes', 'Precision <br> 99%', 'Retention Rate', 'Accuracy <br> 99%']
    body_list = ['97%', '', 'Retention rate measures the percentage of users who continue to use a product or service over time.', '']
    icon_list = ['bell', 'book', 'people', 'download']

    # Create the tile grid component and render it
    tile_grid = TileGrid(num_tiles)
    tile_grid.render(title_list, body_list, icon_list, tile_color=tile_color, tile_shadow=tile_shadow, text_color=text_color)

    # Add a line plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()