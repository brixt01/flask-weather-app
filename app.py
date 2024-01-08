from flask import Flask, render_template
import requests
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator

app = Flask(__name__)

def weekly_plot(x, y):
    fig = Figure()
    ax = fig.subplots()

    ax.plot(y, color="#4066c7")
    ax.xaxis.set_ticks([i*24 for i in range(0, 7)], x)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_ylabel("Temperature (°C)")
    ax.grid(axis="x", which="both")
    
    fig = set_graph_colours(fig, ax, "#12171a", "#252c30", "#f0f8ff")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def daily_plot(x, y):
    fig = Figure()
    ax = fig.subplots()

    ax.plot(y, color="#4066c7")
    ax.set_xticks([i*4 for i in range(0, 7)], x)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_ylabel("Temperature (°C)")
    ax.grid(axis="x", which="both")
    
    fig = set_graph_colours(fig, ax, "#12171a", "#252c30", "#f0f8ff")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def set_graph_colours(fig, ax, outside, inside, labels):
    fig.set_facecolor(outside)      # Outside of graph
    ax.set_facecolor(inside)        # Inside of graph
    for spine in ax.spines.values():        # X and Y major/minor ticks
        spine.set_edgecolor(labels)
    ax.tick_params(axis='x', colors=labels, which="both")       # X tick labels
    ax.tick_params(axis='y', colors=labels, which="both")       # Y tick labels
    ax.xaxis.label.set_color(labels)        # X axis label
    ax.yaxis.label.set_color(labels)        # Y axis label
    return fig

@app.route("/")
def index():
    lat = 53.38
    long = -1.47
    data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m").json()
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    dates = [f"{time[8:10]}/{time[5:7]}" for time in times]
    weekly_temp_plot =  weekly_plot([dates[i*24] for i in range(0, 7)], temps)

    hours = [time[11:16] for time in times]
    daily_temp_plot = daily_plot([hours[i*4] for i in range(0, 7)], temps[0:25])
    
    return render_template("index.html", weekly_temp_plot=weekly_temp_plot, daily_temp_plot=daily_temp_plot, location="Sheffield", lat=lat, long=long)

if __name__ == "__main__":
    app.run(debug=True)