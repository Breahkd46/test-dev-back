import os
# import pickle
import json
import pickle

from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

filename = 'counter.pickle'

# api = Api(app)
if os.path.exists(filename):
    with open(filename, 'rb') as f:
        count = pickle.load(f)
    f.close()
else:
    count = [{"operation": "", "value": '', "counter": 0}]


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/counter')
@cross_origin(support_credentials=True)
def counter():
    counter = count[len(count) - 1]["counter"]
    if 'value' in request.args and 'operation' in request.args:
        try:
            value = int(request.args['value'])
        except ValueError:
            return "Invalid argument : value is not able be parse by integer", 400
        if request.args['operation'] == "ADDITION":
            current_counter = counter + value
        elif request.args['operation'] == "SOUSTRACTION":
            current_counter = counter - value
        elif request.args['operation'] == "MULTIPLICATION":
            current_counter = counter * value
        elif request.args['operation'] == "DIVISION":
            if value == 0:
                return "Invalid argument : value mustn't be 0 to divided", 400
            current_counter = counter / value
        else:
            return f"Invalid arguments : {request.args['operation']} doesn't exist", 400

        count.append({"operation": request.args['operation'],
                      "value": request.args['value'],
                      "counter": current_counter})

        with open(filename, 'wb') as f:
            pickle.dump(count, f)
        f.close()
        return json.dumps(current_counter)
    else:
        return json.dumps(counter)


@app.route('/history', methods=['GET', 'DELETE'])
def history():
    global count
    if request.method == 'GET':
        return json.dumps(count)
    if request.method == 'DELETE':
        count = [{"operation": "", "value": '', "counter": 0}]
        with open(filename, 'wb') as f:
            pickle.dump(count, f)
        f.close()
        return json.dumps(count)


if __name__ == '__main__':
    app.run()
