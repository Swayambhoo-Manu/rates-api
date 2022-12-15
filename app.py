from flask import Flask, jsonify, request
from datetime import datetime

# db module for connection
import db
import psycopg2

app = Flask(__name__)

@app.route("/")
def ratesApi():
    return "Welcome to the rates Api."

@app.route("/rates", methods=["GET"])
def average_price():
    # Fetch Query parameters from the request
    args = request.args
    dateFrom = args.get("date_from")
    dateTo = args.get("date_to")
    origin = args.get("origin")
    destination = args.get("destination")

    # Query parameters validation
    if None in (dateFrom, dateTo):
        return jsonify("Empty dates")

    try:
        format = "%Y-%m-%d"
        dateFromObject = datetime.strptime(dateFrom, format)
        dateToObject = datetime.strptime(dateTo, format)
    except:
        return jsonify("Invalid date format. Please enter date in yyyy-mm-dd format.")

    if origin is None:
        return jsonify("Origin is empty.")

    if destination is None:
        return jsonify("Destination is empty.")

    originPortList = findPortsInRegion(origin)
    # useful in case the origin itself is a port
    originPortList.append(origin)
    originPortTuple = tuple(originPortList)

    destinationPortList = findPortsInRegion(destination)
    # useful in case the destination itself is a port
    destinationPortList.append(destination)
    destinationPortTuple = tuple(destinationPortList)

    connection = db.get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT day, AVG(price), COUNT(price) FROM prices P WHERE orig_code IN %s AND dest_code IN %s AND day >= (%s) AND day <= (%s) GROUP BY day ORDER BY day",
        (
            originPortTuple,
            destinationPortTuple,
            dateFrom,
            dateTo,
        ),
    )
    prices = cursor.fetchall()
    cursor.close()
    connection.close()

    averageDailyPrices = []
    for priceRow in prices:
        d = priceRow[0]
        p = priceRow[1]
        c = priceRow[2]
        p = round(p)
        if c < 3:
            p = "null"

        averageDailyPrices.append(
            {
                "day": str(d),
                "average_price": str(p),
            }
        )
    return jsonify(averageDailyPrices)


# finds all the nodes(ports/regions) in the tree, rooted at the region_code
def find_all_nodes(region_code, visited):
    connection = db.get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT slug FROM regions WHERE parent_slug = (%s)",
        (region_code,),
    )
    regions = cursor.fetchall()
    cursor.close()
    connection.close()
    # base condition for the recursion to stop
    if len(regions) == 0:
        return
    # explore unvisited nodes
    for region_row in regions:
        region = region_row[0]
        if region not in visited:
            visited.add(region)
            find_all_nodes(region, visited)


def findPortsInRegion(region_code):
    visited = set()
    visited.add(region_code)

    # find all the regions, including the regions in between
    find_all_nodes(region_code, visited)
    allRegions = list(visited)

    # find all the ports in these regions
    allPorts = findPortsUnderRegions(allRegions)
    return allPorts


def findPortsUnderRegions(all_regions):
    all_regions_tuple = tuple(all_regions)
    connection = db.get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT code FROM ports WHERE parent_slug IN %s",
        (all_regions_tuple,),
    )
    all_ports = cursor.fetchall()
    cursor.close()
    connection.close()
    all_ports_list = []
    for port in all_ports:
        all_ports_list.append(port[0])
    return all_ports_list


## Extra APIs ( not used )
@app.route("/ports", methods=["GET"])
def getAllPorts():
    connection = db.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ports")
    ports = cursor.fetchall()
    cursor.close()
    connection.close()
    portsJson = jsonify(ports)
    return portsJson


@app.route("/port", methods=["GET"])
def getPort():
    code = request.args.get("code")
    connection = db.get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM ports WHERE code = (%s)",
        (code,),
    )
    ports = cursor.fetchall()
    cursor.close()
    connection.close()
    portsJson = jsonify(ports)
    return portsJson


if __name__ == "__main__":
    app.run(debug=True)
