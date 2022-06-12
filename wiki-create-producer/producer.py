from sseclient import SSEClient as EventSource
from kafka import KafkaProducer


if __name__ == '__main__':
    source_url = 'https://stream.wikimedia.org/v2/stream/page-create'
    event_source = EventSource(source_url)

    prod = KafkaProducer(bootstrap_servers='kafka-server')

    try:
        for event in event_source:
            if event.event == 'message' and event.data:  # first event doesn't have data for some reason
                prod.send('wiki-create', event.data.encode('utf-8'))
    except KeyboardInterrupt:
        prod.close()
