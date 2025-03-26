import pytest
from fastapi import HTTPException, APIRouter
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.routes.metrics import get_pods_details_for_application

# Create a TestClient instance for simulating HTTP requests

router = APIRouter()
client = TestClient(router)


# Mock Kubernetes client
@pytest.fixture
def mock_kubernetes_client():
    with patch("app.main.client") as mock_client:
        mock_metrics_v1 = MagicMock()
        mock_apps_v1 = MagicMock()
        mock_core_v1 = MagicMock()

        mock_client.CustomObjectsApi.return_value = mock_metrics_v1
        mock_client.AppsV1Api.return_value = mock_apps_v1
        mock_client.CoreV1Api.return_value = mock_core_v1

        yield {
            "metrics_v1": mock_metrics_v1,
            "apps_v1": mock_apps_v1,
            "core_v1": mock_core_v1,
        }


# Test get_data_center_metrics endpoint
def test_get_data_center_metrics(mock_kubernetes_client):
    mock_metrics_v1 = mock_kubernetes_client["metrics_v1"]
    mock_metrics_v1.list_namespaced_custom_object.return_value = {
        "items": [
            {
                "metadata": {"name": "pod1"},
                "containers": [{"usage": {"cpu": "500m", "memory": "512Mi"}}]
            }
        ]
    }

    response = client.get("/metrics-individual")
    assert response.status_code == 200
    assert "cpuUsage" in response.json()


# Test getTelemetryData_v2 endpoint
def test_get_telemetry_data_v2(mock_kubernetes_client):
    mock_core_v1 = mock_kubernetes_client["core_v1"]
    mock_core_v1.read_namespaced_pod.return_value.status.phase = "Running"

    response = client.get("/telemetry-individual")
    assert response.status_code == 200
    assert len(response.json()) > 0


# Test get_applications_v2 endpoint
def test_get_applications_v2(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_apps_v1.list_namespaced_deployment.return_value.items = [
        MagicMock(metadata=MagicMock(name="deployment1"))
    ]

    response = client.get("/applications-individual")
    assert response.status_code == 200
    assert len(response.json()) > 0


# Test get_dashboard_metrics endpoint
def test_get_dashboard_metrics():
    response = client.get("/dashboard/metrics")
    assert response.status_code == 200
    assert "system_metrics" in response.json()
    assert "network_metrics" in response.json()
    assert "performance_metrics" in response.json()


# Test get_data_center_metrics_individual endpoint
def test_get_data_center_metrics_individual():
    data_center = "DC-1"
    response = client.get(f"/metrics/{data_center}")
    assert response.status_code == 200
    assert "cpuUsage" in response.json()


# Test get_telemetry_data endpoint
def test_get_telemetry_data():
    data_center = "DC-1"
    response = client.get(f"/telemetry/{data_center}")
    assert response.status_code == 200
    assert len(response.json()) > 0


# Test get_all_metrics endpoint
def test_get_all_metrics():
    response = client.get("/all-metrics")
    assert response.status_code == 200
    assert "DC-1" in response.json()
    assert "DC-2" in response.json()
    assert "DC-3" in response.json()


# Test get_all_telemetry endpoint
def test_get_all_telemetry():
    response = client.get("/all-telemetry")
    assert response.status_code == 200
    assert "DC-1" in response.json()
    assert "DC-2" in response.json()
    assert "DC-3" in response.json()


# Test get_message endpoint
def test_get_message():
    response = client.get("/message")
    assert response.status_code == 200
    assert response.json() == {"message": "Hi, Welcome to the chatbot"}


# Test get_application_details endpoint
@patch("app.main.get_pods_details_for_application")
def test_get_application_details(mock_get_pods_details):
    mock_get_pods_details.return_value = [
        {"name": "pod1", "status": "Running", "memory": 512, "cpu": 500}
    ]

    app_id = "customer-service"
    response = client.get(f"/applications_details?app_id={app_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0


# Test get_pods_details_for_application function
@patch("app.main.create_client")
def test_get_pods_details_for_application(mock_create_client):
    mock_metrics_v1 = MagicMock()
    mock_core_v1 = MagicMock()

    mock_create_client.side_effect = [mock_metrics_v1, MagicMock(), mock_core_v1]

    mock_metrics_v1.list_namespaced_custom_object.return_value = {
        "items": [
            {
                "metadata": {"name": "pod1"},
                "containers": [{"usage": {"cpu": "500m", "memory": "512Mi"}}]
            }
        ]
    }

    mock_core_v1.list_namespaced_pod.return_value.items = [
        MagicMock(metadata=MagicMock(name="pod1"), status=MagicMock(phase="Running"))
    ]

    input_data = '{"app_name": "customer-service"}'
    result = get_pods_details_for_application(input_data)

    assert len(result) > 0
    assert result[0]["name"] == "pod1"