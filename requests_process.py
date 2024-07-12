import requests
import pandas as pd


class RequestsProcess():
    """
    The RequestsProcess class is used to fetch and process weather data from the OpenWeatherMap API.

    Attributes:
        API_KEY (str): API KEY

    Methods:
        get_result(city_name): Returns weather data for a specific city.
        __get_data(response_data): Processes raw data from the API into a meaningful format.
        __split_values(index, info): Extracts and lists values from a specific weather record.
    """

    def __init__(self, API_KEY: str) -> None:
        """
        Constructor for the RequestsProcess class.

        Parameters:
            API_KEY (str): API key.
        """
        self.API_KEY = API_KEY

    def get_result(self, city_name: str) -> pd.DataFrame:
        """
        Fetches and processes weather data for a specific city.

        Parameters:
            city_name (str): The city for which to fetch weather data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing weather data.
        """

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.API_KEY}&units=metric&lang=tr"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}")

        response_json = requests.get(url).json()

        return self.__get_data(response_json)

    def __get_data(self, response_json: dict) -> pd.DataFrame:
        """
        Processes raw weather data from the API into a meaningful format.

        Parameters:
            response_data (dict): Raw weather data from the API.

        Returns:
            pd.DataFrame: A pandas DataFrame containing processed and meaningful weather data.
        """
        all_value_list = []

        for index, info in enumerate(response_json["list"]):
            parsed_values = self.__split_values(index, info)
            all_value_list.append(parsed_values)

        df = pd.DataFrame(all_value_list, columns=["Temperature", "Description", "Image", "Min", "Max", "Date"])
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")

        return df

    def __split_values(self, index: int, info: dict) -> list:
        """
        Extracts and lists values from a specific weather record.

        Parameters:
            index (int): The index of the weather data in the list.
            info (dict): The weather data containing the information.

        Returns:
            list: A list containing temperature, description, image URL, minimum temperature, maximum temperature, and date.
        """
        temp = info["main"]["temp"]
        temp_max = info["main"]["temp_max"]
        temp_min = info["main"]["temp_min"]

        date = info["dt_txt"]

        description = info["weather"][0]["description"]
        icon_name = info["weather"][0]["icon"]

        get_image_url = "http://openweathermap.org/img/wn/" + icon_name + "@2x.png"

        values = [temp, description, get_image_url, temp_min, temp_max, date]

        return values
