
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import requests
import os

app = Flask(__name__)

# Mock function to fetch market prices for a crop
def fetch_market_prices(crop_name):
    # Map crop names to Agmarknet commodity names
    commodity_map = {
        'Tomato': 'Tomato',
        'Potato': 'Potato',
        'Corn': 'Maize',
    }
    commodity = commodity_map.get(crop_name, crop_name)
    api_key = os.environ.get('AGMARKNET_API_KEY')
    endpoint = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'
    today = datetime.today()
    last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, -1, -1)]
    params = {
        'api-key': api_key,
        'format': 'json',
        'filters[commodity]': commodity,
        'limit': 100
    }
    # Only return mock data for all crops
    endpoint = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'
    api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
    params = {
        'api-key': api_key,
        'format': 'json',
        'limit': 100,
        'filters[commodity]': crop_name
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        result = response.json()
        records = result.get('records', [])
        # Get last 7 days in dd/mm/yyyy format
        today = datetime.today()
        last_7_days = [(today - timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
        filtered = [r for r in records if r.get('arrival_date') in last_7_days]
        # Sort by date (latest first)
        filtered.sort(key=lambda x: datetime.strptime(x.get('arrival_date'), '%d/%m/%Y'), reverse=True)
        data = []
        for r in filtered:
            try:
                price = int(float(r.get('modal_price')))
            except:
                continue
            data.append({
                'date': r.get('arrival_date'),
                'price': price,
                'market': r.get('market'),
                'state': r.get('state'),
            })
        return data
    except Exception as e:
        print('API error:', e)
        return []

@app.route('/market', methods=['GET', 'POST'])
def market():
    if request.method == 'POST':
        crop_name = request.form.get('crop') or request.json.get('crop')
        data = fetch_market_prices(crop_name)
        return jsonify(data)
    return render_template('market.html')

if __name__ == '__main__':
    app.run(debug=True)
