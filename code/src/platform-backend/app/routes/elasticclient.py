from elasticsearch import Elasticsearch


# Initialize the Elasticsearch client
def get_elasticsearch_client():
    es = Elasticsearch("http://localhost:9200")  # Use "https://localhost:9200" if security is enabled
    return es
