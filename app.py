from flask import Flask, json, request
from flask_cors import CORS, cross_origin
from multiprocessing import Queue
import time


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

receive_qu = Queue()
send_qu = Queue()


@app.route('/')
@cross_origin()
def hello():
    return "Hello World!"


@app.route('/chat', methods=['POST'])
@cross_origin()
def replyChat():
    print(request.json)
    message = request.json['message']
    userId = request.json['userId']

    send_qu.put(request.json)

    data_received = False
    while not data_received:
        if not receive_qu.empty():
            data = receive_qu.get()
            print('app found data')
            print(data)
            if data['userId'] == userId:
                data_received = True
            else:
                time.sleep(1.)
                receive_qu.put(data)
        else:
            time.sleep(.1)

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=False)
