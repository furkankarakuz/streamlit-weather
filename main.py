import streamlit as st

from city_list import city_list
from requests_process import RequestsProcess

# Request Process
rq = RequestsProcess(st.secrets["API_KEY"])
df = rq.get_result(city_list[0])  # Default Select City


st.markdown("<center><h3>Hava Durumu Tablosu</h3></center>", unsafe_allow_html=True)


# Streamlit Process
def display_weather_info(city_name):
    """
    Fetches and displays weather data for a given city using the RequestsProcess class.

    Parameters:
    city_name (str): The name of the city for which to fetch and display weather data.

    Functions:
    - st_table(): Displays the weather data in a Streamlit dataframe, excluding the image column.
    - get_current(): Displays the current weather conditions in a styled HTML format.
    - st_line(): Displays a line chart of the weather data over time.
    """
    df = rq.get_result(city_name)

    def st_table():
        """
        Displays the weather data in a Streamlit dataframe, excluding the image column.
        """
        st.dataframe(df.drop("Image", axis=1), width=800)

    def get_current():
        """
        Displays the current weather conditions in a styled HTML format.
        """
        current_data = df.iloc[0, :3].tolist()
        st.markdown('<center><div style="display: flex; align-items: center;margin-left: 20%%"><h3>%s&nbsp;°C%s%s</h3><img src="%s"/></div></center>' % (current_data[0], "&nbsp;" * 5, current_data[1].title(), current_data[2]), unsafe_allow_html=True)

    def st_line():
        """
        Displays a line chart of the weather data over time.
        """
        df_melt = df.melt(id_vars=["Date", "Image", "Description"], var_name="Category", value_name="Value")
        df_melt = df_melt.sort_values(["Date", "Category"])
        st.line_chart(df_melt, x="Date", y="Value", color="Category")

    st_table()
    get_current()
    st_line()


# Sidebar City Selection
options = st.sidebar.selectbox("Select a city", city_list)
display_weather_info(options)
