import pandas as pd

class FlightData():
    def __init__(self, path) -> None:
        """Class associated with the loading and feature generation of the flights data corresponding to the DS LATAM challenge

        Args:
            path (str): Path of the .csv file corresponding to the flight data
        """
        self._load_data(path)
        
    
    def _load_data(self, path) -> None:
        self.data = pd.read_csv(path)

