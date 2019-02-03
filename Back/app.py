import os
import pickle
import json

from flask import Flask, request

app = Flask(__name__)
# api = Api(app)
if os.path.exists('counter.cnt'):
    with open('counter.cnt', 'rb') as file:
        count = pickle.load(file)
else:
    count = [{"operation": "", "value": '', "counter": 0}]


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/counter')
def counter():
    counter = count[len(count) - 1]["counter"]
    if 'value' in request.args and 'operation' in request.args:
        try:
            value = int(request.args['value'])
        except ValueError:
            return "Wrong argument"
        if request.args['operation'] == "ADDITION":
            current_counter = counter + value
        elif request.args['operation'] == "SOUSTRACTION":
            current_counter = counter - value
        elif request.args['operation'] == "MULTIPLICATION":
            current_counter = counter * value
        elif request.args['operation'] == "DIVISION":
            current_counter = counter / value
        else:
            return "Wrong parameters"
        count.append({"operation":request.args['operation'],
                      "value": request.args['value'],
                      "counter": current_counter})
        with open('counter.cnt', 'wb') as file:
            pickle.dump(count, file)
        return json.dumps(current_counter)
    else:
        return json.dumps(counter)


@app.route('/history', methods=['GET', 'DELETE'])
def history():
    global count
    if request.method == 'GET':
        return json.JSONEncoder().encode(count)
    if request.method == 'DELETE':
        count = [{"operation": "", "value": '', "counter": 0}]
        with open('counter.cnt', 'wb') as file:
            pickle.dumps(count, file)
        return json.dumps(count)

if __name__ == '__main__':
    app.run()
