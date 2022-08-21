
import datetime
import pandas as pd

class FlightData():
    def __init__(self, path) -> None:
        """Class associated with the loading and feature generation of the flights data corresponding to the DS LATAM challenge

        Args:
            path (str): Path of the .csv file corresponding to the flight data
        """
        self._load_data(path)
        
        # In particular we can check the range of the month using the year, since we know that all of the data is in the year 2017
        # Nevertheless, a more generalized way to check cyclic data is done when generating the time of the day in generate_day_period()
        self.high_season_dates = [[datetime.date(2016,12,15), datetime.date(2017,3,3)],
                                [datetime.date(2017,7,15), datetime.date(2017,7,31)],
                                [datetime.date(2017,9,11), datetime.date(2017,9,30)]]
    
    def _load_data(self, path) -> None:
        self.data = pd.read_csv(path)
        
                
    def convert_dates(self) -> None:
        self.data["Fecha-I"] = pd.to_datetime(self.data["Fecha-I"])
        self.data["Fecha-O"] = pd.to_datetime(self.data["Fecha-O"])


    def generate_seasonality(self):
        """Method used to generate the seasonality feature, we compare each of the "Fecha-I" labels to see if they're in any of the high seasonality ranges defined as a class attribute"""
        
        def _time_in_ranges(date):
            in_ranges = False
            for range in self.high_season_dates:
                in_ranges = in_ranges |  ((range[0] <= date.date()) & (date.date() <= range[1]))
            return in_ranges
        
        self.data["temporada_alta"] = self.data["Fecha-I"].apply(_time_in_ranges)
        
        
    def generate_min_diff(self):
        """Class method used to determine the difference in minutes between the expected takeoff and the real takeoff of the plane"""
        
        # Since we care only about the delays and NOT when the take-off of the flight is earlier than expected,  we don't take the abs value
        diff = self.data["Fecha-O"]-self.data["Fecha-I"]
        
        def diff_to_mins(val):
            return int(val.total_seconds()/60)
        
        self.data["dif_min"] = diff.apply(diff_to_mins)


    def generate_15_delay(self):
        """Class method used to create the boolean to be used as the prediction targets"""
        self.data["atraso_15"] = (self.data["dif_min"]>15)

    
    def generate_day_period(self):
        """For generating the time of the day (mañana, tarde, noche)"""
        
        def _time_in_range(start_time, end_time, time):
            # Since we have to consider the ciclycity/periodicity of the days, we can't just consider the first if, having to check whether the first value of the range is higher or lower than the end value of the range
            if start_time <= end_time:
                # For example between 4am (start) and 8am (end)
                return start_time <= time <= end_time
            else:
                # For example between 9pm (start) and 2am (end)
                return (start_time <= time) | (time <= end_time)


        def _apply_time_check(df_date):
        
            if _time_in_range(datetime.time(5,0), datetime.time(11,59), df_date.time()):
                return "mañana"
            if _time_in_range(datetime.time(12,0), datetime.time(18,59), df_date.time()):
                return "tarde"
            if _time_in_range(datetime.time(19,0), datetime.time(4,59), df_date.time()):
                return "noche"
            
        
        self.data["periodo_dia"] = self.data["Fecha-I"].apply(_apply_time_check)
        
        
    def export_synthetic_features(self, output_path):
        try:
            synthetic_data = self.data[["temporada_alta", "dif_min", "atraso_15", "periodo_dia"]]
            synthetic_data.to_csv(output_path, index=False)
        except KeyError:
            raise KeyError("One of the 4 labels of synthetic data was not correctly generated previously")


        