from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask import Flask, render_template_string
import os
import pandas as pd
import plotly.graph_objects as go
import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"
HEADER = {
    "x-cg-demo-api-key": API_KEY
}

def get_coin_list_with_market_data(body: dict):
    response = requests.get(
        url=f"{BASE_URL}/coins/markets",
        headers=HEADER,
        params=body,
    )


    return response.json()

def get_coin_chart_data(payload: dict, id: str):

    response = requests.get(
        url=f"{BASE_URL}/coins/{id}/market_chart",
        headers=HEADER,
        params=payload,
    )
    return response.json()

def get_asset_platform_data(payload: dict):
    response = requests.get(
        url=f"{BASE_URL}/asset_platforms",
        headers=HEADER,
        params=payload
    )

    return response.json()


@app.route("/")
def home():

        return render_template("home.html")

@app.route("/coins")
def coins():

    coin_list_payload = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,cardano,dogecoin",
        #"name": "Bitcoin,Ethereum,Solana,Cardano,Dogecoin",
        #"symbols": "btc",
    }

    currency = get_coin_list_with_market_data(coin_list_payload)
    print(currency)

    return render_template(
        "index.html",
        currency=currency
    )

@app.route("/asset_platform")
def asset_platform():

    asset_payload = {
        "filter": "nft"
    }

    asset = get_asset_platform_data(asset_payload)

    print(asset)

    return render_template(
        "asset.html",
        asset=asset
    )

def generate_chart_html():

    result = get_coin_chart_data(
        {
            "vs_currency": "usd",
            "days": "1",
            "interval": "hourly",
            "precision": "2"
        },
        "bitcoin"
    )

    df = pd.DataFrame(
        result["prices"],
        columns=["timestamp", "price"]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms"
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price"],
            mode="lines",
            name="Bitcoin"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="Bitcoin Price - Last 24 Hours",
        xaxis_title="Time",
        yaxis_title="Price (USD)"
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )



@app.route("/markets")
def markets():

    #currency = get_coin_list_with_market_data()

    coin_chart_payload = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "hourly",
        "precision": "2"
    }

    coin_id = "bitcoin"

    result = get_coin_chart_data(
        coin_chart_payload,
        coin_id
    )

    df = pd.DataFrame(
        result["prices"],
        columns=["timestamp", "price"]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price"],
            mode="lines",
            name="Bitcoin"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="Bitcoin Price - Last 24 Hours"
    )

    chart = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    return render_template(
        "crypto.html",
        chart=chart)



if __name__ == "__main__":
     app.run(debug=True)






