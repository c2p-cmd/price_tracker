# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx==0.28.1",
#     "marimo>=0.23.5",
#     "numpy==2.4.4",
#     "plotly==6.7.0",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium", app_title="INR Tracker")


@app.cell
def _():
    import marimo as mo
    import httpx
    import numpy as np
    import os

    return httpx, mo, np


@app.cell
def _():
    base_url = 'https://api.frankfurter.dev/v2/rates'
    return (base_url,)


@app.cell
def _():
    import datetime

    current_date = datetime.datetime.now()
    past_date = current_date - datetime.timedelta(days=90)
    current_date_str = current_date.strftime("%Y-%m-%d")
    past_date_str = past_date.strftime("%Y-%m-%d")
    return current_date_str, past_date_str


@app.cell
def _(base_url, current_date_str, httpx, past_date_str):
    request = httpx.get(
        base_url,
        headers={"Content-Type": "application/json"},
        params={
            "base": "INR",
            "quotes": "USD,EUR",
            "from": past_date_str,
            "to": current_date_str,
        },
    )
    return (request,)


@app.cell
def _(np, request):
    euro_rates = []
    usd_rates = []
    euro_dates = []
    usd_dates = []

    for item in request.json():
        date = item["date"]
        if item["quote"] == "USD":
            usd_rates.append(item["rate"])
            usd_dates.append(date)
        elif item["quote"] == "EUR":
            euro_rates.append(item["rate"])
            euro_dates.append(date)

    euro_rates = np.array(euro_rates)
    euro_rates = 1 / euro_rates

    usd_rates = np.array(usd_rates)
    usd_rates = 1 / usd_rates

    euro_dates = np.array(euro_dates)
    usd_dates = np.array(usd_dates)
    return euro_dates, euro_rates, usd_dates, usd_rates


@app.cell
def _(euro_dates, euro_rates, mo, usd_dates, usd_rates):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        x_title="Date",
        y_title="Exchange Rate (INR)",
        subplot_titles=["EUR/INR", "USD/INR"],
    )
    figure.add_trace(
        go.Scattergl(
            x=euro_dates,
            y=euro_rates,
            mode="lines",
            name="EUR/INR",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Scattergl(
            x=usd_dates,
            y=usd_rates,
            mode="lines",
            name="USD/INR",
        ),
        row=2,
        col=1,
    )
    figure.update_layout(
        title="<b>Historical Exchange Rates: EUR/INR and USD/INR</b>",
        legend_title="Currency Pair",
        template="plotly_white",
    )
    mo.ui.plotly(figure)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
