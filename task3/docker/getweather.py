import os
import pyowm

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITY_NAME = os.environ.get('CITY_NAME')


owm = pyowm.OWM(OPENWEATHER_API_KEY)
mgr = owm.weather_manager()
observation = mgr.weather_at_place(CITY_NAME)
w = observation.weather
print('source=openweathermap, city={0}, description={1}, temp={2}, humidity={3}'.format(
       CITY_NAME, w.detailed_status, w.temperature('celsius')['temp'], w.humidity
       )
    )
