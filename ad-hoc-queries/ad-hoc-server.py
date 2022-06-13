from flask import Flask, request, Response
import json
from cassandra_client import CassandraClient


app = Flask(__name__)


@app.route('/', methods=['POST'])
def api():
    try:
        method = getattr(client, f'select_from_{request.form["query_type"]}')
    except AttributeError:
        raise NotImplementedError(request.form["query_type"])

    return Response(json.dumps(method(request.form), indent=4, default=str), mimetype='application/json')


if __name__ == '__main__':
    client = CassandraClient('cassandra-server', 9042, 'project_keyspace')
    client.connect()

    try:
        app.run(host='0.0.0.0', port=5050)
    except KeyboardInterrupt as e:
        client.shutdown()
        raise e
