from unittest.mock import patch, MagicMock
from app.routes.elasticclient import get_elasticsearch_client  # Adjust the import based on your file structure

def test_get_elasticsearch_client():
    # Mock the Elasticsearch class
    with patch("app.main.Elasticsearch") as MockElasticsearch:
        mock_es_instance = MagicMock()
        MockElasticsearch.return_value = mock_es_instance

        # Call the function
        es_client = get_elasticsearch_client()

        # Assertions
        assert es_client == mock_es_instance
        MockElasticsearch.assert_called_once_with("http://localhost:9200")