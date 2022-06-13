from flask import Flask, request, Response
import json


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def serve():
    if request.method == 'POST':
        with open('/opt/app/queries.json', 'w') as f:
            json.dump(request.get_json(), f)
            return Response(status=200)
    else:
        with open('/opt/app/queries.json', 'r') as f:
            return Response(f.read() + '\n', mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1729)
