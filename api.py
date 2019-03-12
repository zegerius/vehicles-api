from flask import Flask, request, jsonify
from data import vehicles

app = Flask(__name__)


@app.route("/", methods=["GET"])
def api():
    """
    Endpoint that returns a list of all vehicles and possible filters.
    Dimensions:
        - brand
        - type
        - color
    """

    data = {}  # returned data

    # Get the applied filters from querystring
    brand_filter = request.args.get("brand")
    color_filter = request.args.get("color")
    type_filter = request.args.get("type")

    # Filters
    f_brand = lambda x: brand_filter in x["brand"]
    f_color = lambda x: color_filter in x["colors"]
    f_type = lambda x: type_filter in x["type"]

    # Decide which filters to use and construct possible filter dimension list.
    #
    # If a filter has been selected for a dimension, return all values
    # If a filter has NOT been selected, only, return the remaining possibilities.
    fs = []
    filters = {}
    if brand_filter:
        fs.append(f_brand)
        filters["brand"] = get_filter(vehicles, "brand")
    if color_filter:
        fs.append(f_color)
        filters["color"] = get_filter(vehicles, "color")
    if type_filter:
        fs.append(f_type)
        filters["type"] = get_filter(vehicles, "type")

    # Apply filters
    data["results"] = list(apply_filter(fs, vehicles))

    # For the filtered data find the possible remaining filters
    data["filters"] = refine_filters(data["results"], filters)

    return jsonify(data)


def get_filter(data: list, f: str):
    """
    Gets possible filters for a specific dimension
    """
    if f == "brand" or f == "type":
        return list(set([vehicle[f] for vehicle in data]))
    if f == "color":
        return list(set([color for vehicle in data for color in vehicle["colors"]]))


def apply_filter(fs: list, data: list):
    """
    Recursively apply filters to data
    """
    if not fs:  # If no filters applied or recursion finished
        return data
    return apply_filter(fs[1:], (x for x in data if fs[0](x)))


def refine_filters(data: list, filters: dict):
    """
    Adds the options that are not filtered yet to the filter list.
    """
    if "brand" not in filters:
        filters["brand"] = get_filter(data, "brand")
    if "type" not in filters:
        filters["type"] = get_filter(data, "type")
    if "color" not in filters:
        filters["color"] = get_filter(data, "color")

    # set() returns unordered, fix that for a consistent experience.
    for f in filters:
        filters[f].sort()

    return filters


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    app.run()
