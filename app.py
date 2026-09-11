from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def home():
    # Free, public API endpoint fetching Bitcoin, Ethereum, and Solana prices in USD
    api_url = "https://coingecko.com"

    try:
        response = requests.get(api_url)
        data = response.json()  # Parse JSON response into a Python dictionary
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = {}

    # Render index.html and inject the live crypto data dictionary into it
    return render_template('index.html', crypto_data=data)


if __name__ == '__main__':
    # Run the server locally on http://127.0.0.1:5000
    app.run(debug=True)