import pytest
from unittest.mock import patch, MagicMock
from app.routes.OpenShiftService import (  # Adjust the import based on your file structure
    get_openshift_tool,
    get_applications,
    get_pods_and_status_health_for_application,
    scale_application_pods,
    restart_application,
    get_deployment_configs,
    upgrade_application,
    check_critical_components_health,
    check_resource_utilization_health,
    deploy_new_application,
    create_client,
    get_metrics_v2,
    get_applications_v2,
)

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


# Test create_client function
def test_create_client(mock_kubernetes_client):
    api_type = "apps"
    client_instance = create_client(api_type)

    assert client_instance == mock_kubernetes_client["apps_v1"]

    api_type = "invalid"
    with pytest.raises(ValueError, match="Invalid API type specified"):
        create_client(api_type)


# Test get_openshift_tool function
@patch("app.main.get_applications")
def test_get_openshift_tool(mock_get_applications, mock_kubernetes_client):
    mock_get_applications.return_value = ["app1", "app2"]
    input_data = '{"tool_name": "get_applications"}'
    response = get_openshift_tool(input_data)
    assert response == ["app1", "app2"]


# Test get_applications function
def test_get_applications(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_apps_v1.list_namespaced_deployment.return_value.items = [
        MagicMock(metadata=MagicMock(name="deployment1")),
        MagicMock(metadata=MagicMock(name="deployment2")),
    ]

    response = get_applications()
    assert len(response) == 2
    assert response[0] == "deployment1"


# Test get_pods_and_status_health_for_application function
def test_get_pods_and_status_health_for_application(mock_kubernetes_client):
    mock_core_v1 = mock_kubernetes_client["core_v1"]
    mock_core_v1.list_namespaced_pod.return_value.items = [
        MagicMock(metadata=MagicMock(name="pod1"), status=MagicMock(phase="Running")),
        MagicMock(metadata=MagicMock(name="pod2"), status=MagicMock(phase="Pending")),
    ]

    input_data = '{"app_name": "customer-service"}'
    response = get_pods_and_status_health_for_application(input_data)
    assert len(response) == 2
    assert response[0]["name"] == "pod1"
    assert response[0]["status"] == "Running"


# Test scale_application_pods function
def test_scale_application_pods(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_deployment = MagicMock(spec=["spec"])
    mock_deployment.spec.replicas = 1
    mock_apps_v1.read_namespaced_deployment.return_value = mock_deployment

    input_data = '{"app_name": "customer-service", "replicas": 3}'
    response = scale_application_pods(input_data)
    assert response == "Successfully scaled customer-service to 3 pods."


# Test restart_application function
def test_restart_application(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_deployment = MagicMock(spec=["spec", "metadata"])
    mock_deployment.spec.template.metadata.annotations = {}
    mock_apps_v1.read_namespaced_deployment.return_value = mock_deployment

    input_data = '{"app_name": "customer-service"}'
    response = restart_application(input_data)
    assert response == "Successfully restarted customer-service."


# Test get_deployment_configs function
def test_get_deployment_configs(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_deployment = MagicMock(
        spec=["spec", "metadata"],
        spec_replicas=2,
        spec_strategy={"type": "RollingUpdate"},
        metadata=MagicMock(labels={"label1": "value1"}, annotations={"annotation1": "value1"}),
        spec_template_spec_containers=[
            MagicMock(name="container1", image="image1", ports=[MagicMock(container_port=8080)]),
        ],
    )
    mock_apps_v1.read_namespaced_deployment.return_value = mock_deployment

    input_data = '{"app_name": "customer-service"}'
    response = get_deployment_configs(input_data)
    assert response["replicas"] == 2
    assert response["containers"][0]["name"] == "container1"


# Test upgrade_application function
def test_upgrade_application(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_deployment = MagicMock(spec=["spec", "metadata"])
    mock_deployment.spec.template.spec.containers = [MagicMock(image="old_image")]
    mock_apps_v1.read_namespaced_deployment.return_value = mock_deployment

    input_data = '{"app_name": "customer-service", "new_image": "new_image"}'
    response = upgrade_application(input_data)
    assert response == "Successfully upgraded customer-service to image new_image."


# Test check_critical_components_health function
def test_check_critical_components_health(mock_kubernetes_client):
    mock_core_v1 = mock_kubernetes_client["core_v1"]
    mock_core_v1.api_client.call_api.return_value = ("Healthy", 200)

    response = check_critical_components_health()
    assert response["status"] == "Healthy"


# Test check_resource_utilization_health function
def test_check_resource_utilization_health(mock_kubernetes_client):
    mock_metrics_v1 = mock_kubernetes_client["metrics_v1"]
    mock_metrics_v1.list_cluster_custom_object.side_effect = [
        {"items": [{"metadata": {"name": "node1"}, "usage": {"cpu": "50n", "memory": "50Ki"}}]},
        {"items": [{"metadata": {"name": "pod1"}, "containers": [{"usage": {"cpu": "50n", "memory": "50Ki"}}]}]},
    ]

    response = check_resource_utilization_health()
    assert response["status"] == "Healthy"


# Test deploy_new_application function
def test_deploy_new_application(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_core_v1 = mock_kubernetes_client["core_v1"]

    input_data = '{"app_name": "new-app", "container_image": "new-image", "replicas": 2, "port": 8080}'
    response = deploy_new_application(input_data)
    assert response == "Successfully deployed application 'new-app' with 2 replicas."


# Test get_metrics_v2 function
def test_get_metrics_v2(mock_kubernetes_client):
    mock_metrics_v1 = mock_kubernetes_client["metrics_v1"]
    mock_metrics_v1.list_namespaced_custom_object.return_value = {
        "items": [
            {
                "metadata": {"name": "pod1"},
                "containers": [{"usage": {"cpu": "50n", "memory": "50Ki"}}],
            }
        ]
    }

    response = get_metrics_v2()
    assert response["cpuUsage"] == [50]


# Test get_applications_v2 function
def test_get_applications_v2(mock_kubernetes_client):
    mock_apps_v1 = mock_kubernetes_client["apps_v1"]
    mock_apps_v1.list_namespaced_deployment.return_value.items = [
        MagicMock(
            metadata=MagicMock(name="deployment1", creation_timestamp="2023-10-01"),
            status=MagicMock(available_replicas=1),
        )
    ]
    mock_metrics_v1 = mock_kubernetes_client["metrics_v1"]
    mock_metrics_v1.list_namespaced_custom_object.return_value = {
        "items": [
            {
                "metadata": {"name": "pod1"},
                "containers": [{"usage": {"cpu": "50n", "memory": "50Ki"}}],
            }
        ]
    }

    response = get_applications_v2()
    assert len(response) > 0
    assert response[0]["application"]["name"] == "deployment1"