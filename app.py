from flask import Flask, render_template, request, jsonify
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point

from graph import G, graph, nodes
from dijkstra import dijkstra

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def get_nearest_node(lat, lon):
    """
    Find the nearest node using GeoPandas.
    """

    point = Point(lon, lat)

    distances = nodes.geometry.distance(point)

    nearest_node = distances.idxmin()

    return nearest_node


@app.route("/route", methods=["POST"])
def route():

    data = request.get_json()

    start = data["start"] + ", Kolkata, India"
    end = data["end"] + ", Kolkata, India"

    try:

        start_location = ox.geocode(start)
        end_location = ox.geocode(end)

    except Exception:

        return jsonify({
            "success": False,
            "message": "Location not found."
        })

    start_node = get_nearest_node(
        start_location[0],
        start_location[1]
    )

    end_node = get_nearest_node(
        end_location[0],
        end_location[1]
    )

    print("Start Node:", start_node)
    print("End Node:", end_node)

    path, total_distance = dijkstra(
        graph,
        start_node,
        end_node
    )

    if path is None:

        return jsonify({
            "success": False,
            "message": "No path found."
        })

    route_coordinates = []

    for node in path:

        route_coordinates.append([
            G.nodes[node]["y"],
            G.nodes[node]["x"]
        ])

    return jsonify({

        "success": True,

        "distance": round(total_distance / 1000, 2),

        "route": route_coordinates

    })


if __name__ == "__main__":
    app.run(debug=True)