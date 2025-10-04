# PredictaStorm
🌩️ PredictaStorm: Date-Specific Weather Forecast Application
Mission Statement: "Because every drop counts!" ☔✨

PredictaStorm is a full-stack web application developed by Team PredictaStorm to deliver reliable, user-friendly, hourly weather predictions. Our goal is to answer the timeless question, "Will it rain on my parade?", by helping users plan their days with confidence. The application focuses on providing date-specific hourly forecasts for up to 5 days, simplifying complex data into clear, actionable insights.

✨ Key Features
This application offers essential tools for quick and accurate planning:

- Focused Forecasting: Users can easily request hourly weather data (Temperature, Humidity, Icons) for a specific city and date within the 5-day forecast window.

- Visual Rain Alerts: The application immediately highlights any hourly forecast period where rain, drizzle, or showers are predicted, ensuring users never miss a weather alert.

- Seamless User Experience (SPA): Built as a Single-Page Application using pure JavaScript, the interface provides smooth navigation between the Home (Forecast) page, the About Us page, and the Contact Us section.

- Modern Design: The entire application uses Tailwind CSS for a clean, responsive, and mobile-first design.

💻 Technology & Architecture
The PredictStorm application utilizes a modern, decoupled architecture:

- Frontend: The user interface is built exclusively with HTML5, CSS3, and Vanilla JavaScript. We rely on Tailwind CSS for efficient styling and maintain all view management entirely in the client-side JavaScript.

- Backend (API Server): A robust RESTful API server developed using Python Flask. This server acts as a crucial intermediary, securing the API key and handling all external data requests and necessary validation before serving processed data to the frontend.

- Data Source: All real-time global weather data is sourced from the OpenWeatherMap API, which provides the base 5-day, 3-hour step forecast.

🚀 Setup and Local Development Guide
To run PredictStorm locally, you need Python (with Flask, Flask-CORS, and Requests) installed.

1. Backend Setup
The Python Flask server must be running first on port 5000.

- Install Dependencies: Run the following command in your terminal:

    pip install Flask flask-cors requests

- API Key Configuration: Ensure your OpenWeatherMap API key is correctly defined within your backend file (api/forecast.py or main.py).

- Start the Server: Execute the Python script to start the server:

    python main.py
    # or python api/forecast.py (depending on your file structure)

    The server will start at http://127.0.0.1:5000.

2. Frontend Access
The frontend is contained in a single HTML file.

- Launch the App: Simply open the index.html file directly in your web browser.

- API Connection: The application is automatically configured to fetch data from the running backend server at http://127.0.0.1:5000/api/forecast.

👥 Meet the PredictaStorm Team
We’re dreamers, doers, and problem-solvers united by a passion for data and creating technology that genuinely improves lives. Our curiosity drives us to explore the science of weather forecasting and transform it into simple tools everyone can use.

Here are the six passionate innovators behind PredictStorm:

- Bhumika Vadchhak
- Krishna Hadiya
- Krisha Simariya
- Om Makwana
- Het Patel 
- Dhruv Patel

© 2025 PredictaStorm Team.
