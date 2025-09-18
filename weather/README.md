# Crop Disease Forecaster 🌱

A Flask web application that predicts crop diseases based on weather conditions and provides farmers with expert recommendations for healthy farming practices.

## Features

- **Weather Analysis**: Get 3-day weather forecast using WeatherAPI.com
- **Disease Prediction**: Advanced algorithms analyze weather conditions to predict potential crop diseases
- **Risk Assessment**: Categorize disease risks as Low, Medium, or High
- **Expert Advice**: Get eco-friendly remedies and preventive measures
- **Clean UI**: Modern Bootstrap-based responsive design
- **Print Support**: Generate printable reports for field reference

## Supported Diseases

The application monitors and predicts the following crop diseases:

- **Powdery Mildew** (High Risk) - Fungal disease affecting leaves and stems
- **Leaf Spot** (High Risk) - Dark spots on leaves caused by fungi
- **Mites Infestation** (High Risk) - Tiny pests causing leaf damage
- **Leaf Curl** (Medium Risk) - Leaves curling due to heat stress
- **Blight** (High Risk) - Rapid plant death due to excessive moisture
- **Root Rot** (High Risk) - Root system damage from waterlogging
- **Anthracnose** (Medium Risk) - Fungal disease in high humidity
- **Frost Damage** (High Risk) - Cold damage to plant tissues

## Weather Conditions Analysis

The app analyzes weather conditions to predict diseases:

- **High Fungal Risk**: Humidity > 80% and temperature 20-30°C
- **Mites/Leaf Curl Risk**: Temperature > 32°C and dry conditions
- **Blight/Root Rot Risk**: Continuous rain (>5mm)
- **Additional Conditions**: High humidity (>90%), low temperature (<10°C)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd crop-disease-forecaster
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `env.example` to `.env`
   - Get your OpenWeatherMap API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Update the `.env` file with your API key:
     ```
     SECRET_KEY=your-secret-key-here
     OPENWEATHER_API_KEY=your-openweathermap-api-key-here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Enter Location**: On the homepage, enter your city or village name
2. **Check Risk**: Click "Check Risk" to analyze weather conditions
3. **View Results**: Review the 3-day weather forecast and disease risk analysis
4. **Follow Precautions**: Implement the recommended preventive measures

## API Configuration

### WeatherAPI.com

1. Visit [WeatherAPI.com](https://www.weatherapi.com/my/)
2. Sign up for a free account
3. Generate an API key
4. Add the key to your `.env` file

**Note**: The free tier allows 1 million API calls per month, which is more than sufficient for testing and production use.

## Project Structure

```
crop-disease-forecaster/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
└── templates/
    ├── base.html         # Base template with Bootstrap
    ├── index.html        # Homepage template
    └── results.html      # Results page template
```

## Dependencies

- **Flask 2.3.3**: Web framework
- **requests 2.31.0**: HTTP library for API calls
- **python-dotenv 1.0.0**: Environment variable management

## Features in Detail

### Weather Integration
- Fetches 3-day weather forecast from OpenWeatherMap
- Analyzes temperature, humidity, and rainfall data
- Handles API errors gracefully with user-friendly messages

### Disease Analysis
- Implements rule-based disease prediction algorithms
- Considers multiple weather factors for accurate predictions
- Provides risk levels (Low/Medium/High) for each disease

### User Interface
- Responsive Bootstrap design
- Clean, modern interface suitable for farmers
- Print-friendly results page
- Mobile-optimized layout

### Precautions & Recommendations
- Categorized advice (Preventive Measures, Eco-friendly Remedies, etc.)
- Practical tips for farmers
- Focus on sustainable and organic solutions

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenWeatherMap API key is correctly set in `.env`
   - Check if the API key is valid and active

2. **Location Not Found**
   - Try using more specific location names
   - Include country name if needed (e.g., "Mumbai, India")

3. **No Weather Data**
   - Check your internet connection
   - Verify the API key has sufficient quota

### Error Messages

- **"Weather API key not configured"**: Set your API key in `.env` file
- **"Unable to fetch weather data"**: Check location name and internet connection
- **"Please enter a location"**: Fill in the location field before submitting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions:
- Check the troubleshooting section above
- Review the OpenWeatherMap API documentation
- Open an issue in the repository

## Future Enhancements

- Database integration for storing historical data
- More sophisticated machine learning models
- Support for specific crop types
- Mobile app version
- Integration with IoT sensors
- Multi-language support

---

**Built with ❤️ for farmers and sustainable agriculture**
