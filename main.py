# Conceptual Python Backend using Flask
# This file serves as the API server that your frontend (index.html) connects to.
# It hides the API key and performs the necessary data retrieval and filtering.

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, date, timedelta # Added timedelta for date calculations

# 1. Initialize Flask App
app = Flask(__name__)
# IMPORTANT: CORS is enabled to allow your JavaScript frontend (running on a 
# different origin, i.e., in the Canvas preview) to communicate with this 
# local Flask server (running on 127.0.0.1:5000).
CORS(app) 

# 2. Configuration (Using the API key you provided)
# NOTE: This key is exposed in the file, but is fine for this environment.
OPENWEATHERMAP_API_KEY = "962131ee9b3221425bb8ddf311ef2014" 
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast" # 5-day / 3-hour forecast
MAX_FORECAST_DAYS = 5 # OpenWeatherMap limit (including today)

# 3. Define the API Endpoint for Specific Date Forecast
@app.route('/api/forecast', methods=['GET'])
def get_date_forecast():
    """
    Fetches 5-day / 3-hour step forecast data from OpenWeatherMap 
    and returns the entries corresponding to the requested date.
    
    Query example: /api/forecast?city=London&date=2025-10-07
    """
    city = request.args.get('city')
    date_str = request.args.get('date') # Expected format: YYYY-MM-DD
    
    if not city or not date_str:
        return jsonify({"error": "Missing required parameters: 'city' and 'date'"}), 400

    # 3a. Validate and Parse Date
    try:
        # We only need the date part (YYYY-MM-DD) for filtering
        target_date: date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
    # 3b. NEW PREVENTATIVE CHECK: Ensure the requested date is within the 5-day limit
    today = datetime.now().date()
    # Calculate the maximum future date allowed (Today + 4 days)
    max_date_allowed = today + timedelta(days=MAX_FORECAST_DAYS - 1)
    
    if target_date > max_date_allowed:
        # Calculate how many days out the target date is for the error message
        days_out = (target_date - today).days
        return jsonify({
            "error": f"The requested date ({date_str}) is {days_out} days out. Forecast is limited to {MAX_FORECAST_DAYS} days, up to {max_date_allowed.strftime('%Y-%m-%d')}."
        }), 400
    
    # 3c. Construct API Request
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric' # Request temperature in Celsius
    }
    
    try:
        # Make the request to the external weather service
        response = requests.get(BASE_FORECAST_URL, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        forecast_data = response.json()
        
        # Check for non-200 API response codes within the JSON data
        if forecast_data.get('cod') != '200' and response.status_code == 200:
             # Handle API-specific errors like "city not found"
             return jsonify({"error": forecast_data.get('message', 'Could not retrieve forecast data')}), 404
             
        # 3d. Filter Data for the Target Date
        daily_forecasts = []
        for item in forecast_data.get('list', []):
             # item['dt_txt'] is in "YYYY-MM-DD HH:MM:SS" format
             item_date: date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
             
             if item_date == target_date:
                 daily_forecasts.append({
                     "time": item['dt_txt'].split(' ')[1][:5], # Extract just the HH:MM
                     "temp": item['main']['temp'],
                     "description": item['weather'][0]['description'],
                     "icon": item['weather'][0]['icon'],
                     "humidity": item['main']['humidity'], # Humidity is already a percentage (0-100)
                 })

        if not daily_forecasts:
            # This happens if the city is found but the date is *just* outside the 5-day window
            # (which should now be mostly caught by the pre-emptive check)
            return jsonify({"error": f"No forecast data available for {date_str} in {city}. The API limit was likely reached."}), 404
        
        # 3e. Return Filtered Data
        return jsonify({
            "city": forecast_data['city']['name'],
            "country": forecast_data['city']['country'],
            "date": date_str,
            "hourly_data": daily_forecasts
        })

    except requests.exceptions.HTTPError as e:
        # Log the error for debugging purposes
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        # Handle standard HTTP errors (like 401 Unauthorized if the API key is bad)
        return jsonify({"error": f"Weather API HTTP Error: {response.status_code} - Check API key or city name."}), response.status_code
        
    except requests.exceptions.RequestException as e:
        # Handle network issues (e.g., DNS error, connection timeout)
        print(f"Network Error: {e}")
        return jsonify({"error": f"A network error occurred connecting to the external weather API: {e}"}), 500

# 4. Run the application
if __name__ == '__main__':
    # Flask will run on this address, which is where the JavaScript frontend will look.
    app.run(debug=True, host='127.0.0.1', port=5000)
