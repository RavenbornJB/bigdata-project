from flask import Flask, request
from cassandra_client import CassandraClient


app = Flask(__name__)


@app.route('/', methods=['POST'])
def api():

    method = None
    try:
        method = getattr(client, f'select_from_{request.form["query_type"]}')
    except AttributeError:
        raise NotImplementedError(request.form["query_type"])

    return dumps(method(request.form), indent=4, default=str)


if __name__ == '__main__':
    client = CassandraClient('cassandra-server', 9042, 'project')
    client.connect()

    try:
        app.run(host='0.0.0.0', port=5050)
    except KeyboardInterrupt as e:
        client.shutdown()
        raise e