from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import datetime
from pydantic import BaseModel
from typing import List, Optional
import time

# Load database into memory
print('Loading database into memory...')
source = sqlite3.connect('data/combined/combined.db', check_same_thread=False)
connection = sqlite3.connect(':memory:', check_same_thread=False)
source.backup(connection)
cursor = connection.cursor()

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/api/docs")
def docs():

    docs = {
        '/api/houses': {
            'Args': [
                "price_min", 
                "price_max",
                "date_min",
                "date_max",
                "is_new",
                "was_new",
                "postcode",
                "paon",
                "saon",
                "street",
                "locality",
                "town_city",
                "district",
                "county",
                "ppd_category_type",
                "record_status",
                "latitude",
                "longitude",
                "start",
                "length",
            ]
        }
    }

    return jsonify(docs)

@app.route("/api/houses", methods=["GET"])
def houses():
    return jsonify(GetHouses(json.loads(json.dumps(request.args))))

def GetHouses(parameters: dict) -> str:

    # Set request start time
    start_time = time.time()

    class Transaction(BaseModel):

        id: str
        price: int
        date: datetime.datetime
        is_new: bool

    class House(BaseModel):

        transactions: List[Transaction] = []
        postcode: Optional[str] = None
        property_type: Optional[str] = None
        tenure: Optional[str] = None
        paon: Optional[str] = None
        saon: Optional[str] = None
        street: Optional[str] = None
        locality: Optional[str] = None
        town_city: Optional[str] = None
        district: Optional[str] = None
        county: Optional[str] = None
        ppd_category_type: Optional[str] = None
        record_status: Optional[str] = None
        latitude: Optional[float] = None
        longitude: Optional[float] = None

    class HousesResponse(BaseModel):

        houses: List[House] = []
        response_time: Optional[str] = None

    # Filters
    _price_min = parameters.get("price_min")
    _price_max = parameters.get("price_max")
    _date_min = parameters.get("date_min")
    _date_max = parameters.get("date_max")
    _is_new = parameters.get("is_new")
    _postcode = parameters.get("postcode")
    _paon = parameters.get("paon")
    _saon = parameters.get("saon")
    _street = parameters.get("street")
    _locality = parameters.get("locality")
    _town_city = parameters.get("town_city")
    _district = parameters.get("district")
    _county = parameters.get("county")
    _ppd_category_type = parameters.get("ppd_category_type")
    _record_status = parameters.get("record_status")
    _latitude = parameters.get("latitude")
    _longitude = parameters.get("longitude")
    _start = parameters.get("start", 0)
    _length = parameters.get("length", 100)

    filters = [
        { "Name": "price", "Value": _price_min, "Type": "Integer", "Operator": ">=" },
        { "Name": "price", "Value": _price_max, "Type": "Integer", "Operator": "<=" },
        { "Name": "date", "Value": _date_min, "Type": "Date", "Operator": ">=" },
        { "Name": "date", "Value": _date_max, "Type": "Date", "Operator": "<=" },
        { "Name": "is_new", "Value": _is_new, "Type": "Boolean" },
        { "Name": "postcode", "Value": _postcode, "Type": "String" },
        { "Name": "paon", "Value": _paon, "Type": "String" },
        { "Name": "saon", "Value": _saon, "Type": "String" },
        { "Name": "street", "Value": _street, "Type": "String" },
        { "Name": "locality", "Value": _locality, "Type": "String" },
        { "Name": "town_city", "Value": _town_city, "Type": "String" },
        { "Name": "district", "Value": _district, "Type": "String" },
        { "Name": "county", "Value": _county, "Type": "String" },
        { "Name": "ppd_category_type", "Value": _ppd_category_type, "Type": "String" },
        { "Name": "record_status", "Value": _record_status, "Type": "String" },
        { "Name": "latitude", "Value": _latitude, "Type": "Float" },
        { "Name": "longitude", "Value": _longitude, "Type": "Float" }
    ]

    dynamic_filter_string = ""

    isFirst = True
    values = []

    for filter in filters:

        if filter["Value"] is not None:

            if isFirst:
                dynamic_filter_string += " WHERE "
                isFirst = False
            else:
                dynamic_filter_string += " AND "

            filter_name = filter["Name"]
            filter_value = filter["Value"]

            if filter["Type"] == "Integer":

                filter_value = int(filter_value)
                filter_operator = filter["Operator"]

                dynamic_filter_string += f"CAST ({filter_name} AS INTEGER) {filter_operator} ?"
                values.append(filter_value)
                isFirst = False

            if filter["Type"] == "Float":

                filter_value = float(filter_value)
                filter_operator = filter["Operator"]

                dynamic_filter_string += f"CAST ({filter_name} AS FLOAT) {filter_operator} ?"
                values.append(filter_value)
                isFirst = False
                
            elif filter["Type"] == "Date":

                filter_operator = filter["Operator"]

                dynamic_filter_string += f"{filter_name} {filter_operator} ?"
                values.append(filter_value)
                isFirst = False
                
            else:

                if filter["Type"] == "Boolean":

                    if bool(filter_value) == True:
                        filter_value = "Y"
                    else:
                        filter_value = "N"

                dynamic_filter_string += f"{filter_name} LIKE ?"
                values.append(f"%{filter_value}%")
                isFirst = False

    # Get data which matches the filters
    query_string = f"SELECT * FROM combined {dynamic_filter_string}"

    if _length != 'all':
        query_string += f" LIMIT {_length}"
    
    if _start:
        query_string += f" OFFSET {_start}"
    
    cursor.execute(query_string, values)
    
    # Get results
    results = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

    # Convert results to houses
    houses = []   

    for result in results:

        house = House(
            transactions=[],
            postcode=result["postcode"],
            property_type=result["property_type"],
            tenure=result["tenure"],
            paon=result["paon"],
            saon=result["saon"],
            street=result["street"],
            locality=result["locality"],
            town_city=result["town_city"],
            district=result["district"],
            county=result["county"],
            ppd_category_type=result["ppd_category_type"],
            record_status=result["record_status"],
            latitude=result["latitude"],
            longitude=result["longitude"],
        )

        # check if house is already in houses
        already_exists = False
        for existing_house in houses:

            if existing_house.postcode == house.postcode and existing_house.property_type == house.property_type and existing_house.paon == house.paon and existing_house.saon == house.saon:
                already_exists = True
                house = existing_house
                break

        if not already_exists:
            houses.append(house)

        house.transactions.append(
            Transaction(
                id=result["transfer_uid"],
                price=result["price"],
                date=result["date"],
                is_new=result["is_new"]
            )
        )

    # Calculate response time in milliseconds as an integer
    response_time = f"{int((time.time() - start_time) * 1000)}ms"

    # Return json
    return json.loads(HousesResponse(houses=houses, response_time=response_time).json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)