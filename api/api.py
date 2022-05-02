from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import datetime
from pydantic import BaseModel
from typing import List, Optional, Union
import time

# Load database into memory
print('Loading database into memory...')
source = sqlite3.connect('/data/database.db', check_same_thread=False)
connection = sqlite3.connect(':memory:', check_same_thread=False)
source.backup(connection)

app = Flask(__name__)
CORS(app)

class Transaction(BaseModel):
    
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
    id: Optional[str] = None
    price: Optional[int] = None
    date: Union[datetime.datetime, str] = None
    is_new: Optional[bool] = None

class TransactionsResponse(BaseModel):

    transactions: List[Transaction] = []
    response_time: Optional[str] = None
    count: Optional[int] = None

@app.route("/")
@app.route("/docs")
def docs():

    docs = {
        '/transactions': {
            'Args': [
                "price_min", 
                "price_max",
                "date_min",
                "date_max",
                "is_new",
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

@app.route("/transactions", methods=["GET"])
def transactions():
    return jsonify(GetTransactions(json.loads(json.dumps(request.args))))   

def GetTransactions(parameters: dict) -> str:

    # Set request start time
    start_time = time.time()

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
        { "Name": "postcode", "Value": _postcode, "Type": "String" },
        { "Name": "paon", "Value": _paon, "Type": "String" },
        { "Name": "saon", "Value": _saon, "Type": "String" },
        { "Name": "street", "Value": _street, "Type": "String" },
        { "Name": "locality", "Value": _locality, "Type": "String" },
        { "Name": "town_city", "Value": _town_city, "Type": "String" },
        { "Name": "district", "Value": _district, "Type": "String" },
        { "Name": "county", "Value": _county, "Type": "String" },
        { "Name": "is_new", "Value": _is_new, "Type": "Boolean" },
        { "Name": "ppd_category_type", "Value": _ppd_category_type, "Type": "String" },
        { "Name": "record_status", "Value": _record_status, "Type": "String" },
        { "Name": "latitude", "Value": _latitude, "Type": "Float" },
        { "Name": "longitude", "Value": _longitude, "Type": "Float" },
        { "Name": "price", "Value": _price_min, "Type": "Integer", "Operator": ">=" },
        { "Name": "price", "Value": _price_max, "Type": "Integer", "Operator": "<=" },
        { "Name": "date", "Value": _date_min, "Type": "Date", "Operator": ">=" },
        { "Name": "date", "Value": _date_max, "Type": "Date", "Operator": "<=" },
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

    cursor = connection.cursor()

    print(f"\nQuery String: {query_string}")
    
    cursor.execute(query_string, values)

    process_time = time.time()

    # Iterate through rows
    transactions = []
    for row in cursor:

        try:
            house = Transaction(
                postcode=row[4],
                property_type=row[5],
                tenure=row[7],
                paon=row[8],
                saon=row[9],
                street=row[10],
                locality=row[11],
                town_city=row[12],
                district=row[13],
                county=row[14],
                ppd_category_type=row[15],
                record_status=row[16],
                latitude=row[17],
                longitude=row[18],
                id=row[1],
                price=row[2],
                date=row[3],
                is_new=row[6],
            )

            transactions.append(house)
        except Exception as e:
            print(e)

    # Print total number of rows processed
    print(f"Total number of rows processed: {len(transactions)}")

    # Calculate response time in milliseconds as an integer
    response_time = f"{int((time.time() - start_time) * 1000)}ms"

    print("Created transactions list in " + str(time.time() - process_time) + " seconds")

    process_time = time.time()

    json_data = json.loads(TransactionsResponse(transactions=transactions, response_time=response_time, count=len(transactions)).json())

    print("Created response json in " + str(time.time() - process_time) + " seconds")

    # Return json
    return json_data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)