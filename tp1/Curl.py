import  requests
import  os

 # affectation des variables d'environnement dans des variables python 
 
APIKEY = os.environ['APIKEY'] 
LAT = os.environ['LAT']
LONG = os.environ['LONG']


response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"&appid="+APIKEY)

print(response.status_code)
print(response.json())

"""
import  requests
import  os




url = "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"appid="+api_key

response = requests.get(url)

print(response.status_code)
print(response.json())
"""
