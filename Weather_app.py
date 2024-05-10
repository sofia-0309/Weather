from flask import Flask, request, render_template,url_for
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    
    if request.method == 'POST':
        city = request.form['city']
        api_key = "1f5cd58b97fb46ebbd9205406240205"
        api_link = "http://api.weatherapi.com/v1/current.json"
        forecast_url = "http://api.weatherapi.com/v1/forecast.json"

        params = {
            'key': api_key,
            'q': city,
            'days':1,
            
        }
        image_url = f"https://source.unsplash.com/1600x900/?{city}"
        forecast_response = requests.get(forecast_url, params=params)
        response = requests.get(api_link, params=params)
        if response.status_code == 200 or forecast_response.status_code==200:
            weather_data = response.json()
            future_data = forecast_response.json()
            hourly_forecast = next((hour for hour in future_data['forecast']['forecastday'][0]['hour'] if hour['time'].endswith('23:00')), None)
            weather = {
                
                'humidity':weather_data['current']["humidity"],
                'time':weather_data['location']['localtime'][-5:],
                'wind':weather_data['current']["wind_kph"],
                'location': weather_data["location"]["name"],
                'temperature': weather_data["current"]["temp_c"],
                'condition': weather_data["current"]["condition"]["text"],
                'icon': weather_data["current"]["condition"]["icon"],
                
            }
            forecast={
                'humidity':hourly_forecast["humidity"],
                'temp_for':hourly_forecast[ 'temp_c'],
                'condition_for':hourly_forecast["condition"]["text"],
                'icon': hourly_forecast["condition"]["icon"],
                'wind':hourly_forecast["wind_kph"],
                
            }

            if forecast:
                return render_template('index.html', weather=weather, forecast=forecast,image_url=image_url)
            else:
            
                return render_template('index.html', weather=weather,image_url=image_url)
        else:
            return "Failed to retrieve weather data"
    
    return render_template('index.html', weather=None)

@app.route('/forecast',methods=['GET', 'POST'])
def forecast():

    if request.method == 'POST':
        city = request.form['city']
        api_key = "1f5cd58b97fb46ebbd9205406240205"
        api_link = "http://api.weatherapi.com/v1/current.json"
        forecast_url = "http://api.weatherapi.com/v1/forecast.json"
        image_url = f"https://source.unsplash.com/1600x900/?{city}"
        params = {
            'key': api_key,
            'q': city,
            'days':1,
            
        }
        current_response = requests.get(api_link, params=params)
        weather_data = current_response.json()
        forecast_response = requests.get(forecast_url, params=params)
    
        curr_time = weather_data['location']['localtime']
       # curr_time = datetime.strptime(curr_time, '%Y-%m-%d %H:%M').time()
     
        if forecast_response.status_code==200:
            
            future_data = forecast_response.json()
            hourly_forecast = [hour for hour in future_data['forecast']['forecastday'][0]['hour']
                                if hour['time'] > curr_time] 

            return render_template('forecast.html', hourly_forecast=hourly_forecast, city=city,curr_time=curr_time,
                                   image_url=image_url)
        else:
            return "Failed to retrieve weather data"

            
        
    return render_template('forecast.html', hourly_forecast=None)

if __name__ == "__main__":
    app.run(debug=True)