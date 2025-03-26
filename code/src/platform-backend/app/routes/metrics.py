import json

from fastapi import APIRouter
import random
import datetime
from kubernetes.client import Configuration
import pandas as pd
import time
from kubernetes import client, config
from datetime import datetime, timedelta
import random

router = APIRouter()


def create_client(api_type):
    try:
        # Authenticate using OpenShift token and server details
        token = "sha256~SYr05fXxf6tP3a920g4eMjcEwm152xtdCZzy09A-EFE"
        server = "https://api.rm2.thpm.p1.openshiftapps.com:6443"

        # Create configuration object
        configuration = Configuration()
        configuration.host = server
        configuration.verify_ssl = False  # Disable SSL verification if necessary
        configuration.api_key = {"authorization": f"Bearer {token}"}

        # Use the configuration
        client.Configuration.set_default(configuration)

        if api_type == 'apps':
            return client.AppsV1Api()
        elif api_type == 'core':
            return client.CoreV1Api()
        elif api_type == 'metrics':
            return client.CustomObjectsApi()
        else:
            raise ValueError("Invalid API type specified.")
    except Exception as e:
        print(f"Error creating client: {str(e)}")
        return None


def get_metrics_v2(input=None):
    namespace = "mindovermachinestech-dev"
    metrics_v1 = create_client('metrics')
    cpu_usage = []
    memory_usage = []
    timestamps = []

    try:
        metrics = metrics_v1.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )
        print(metrics)
        for pod in metrics.get("items", []):
            pod_name = pod["metadata"]["name"]
            for container in pod.get("containers", []):
                # Extract CPU and memory usage
                name = container["name"]
                cpu = container["usage"]["cpu"]
                memory = container["usage"]["memory"]
                cpu_millicores = int(cpu.rstrip("n").rstrip("m")) if cpu.endswith("n") else int(cpu) * 1000
                memory_mb = int(memory.rstrip("Ki").rstrip("Mi").rstrip("Gi")) if memory.endswith("Ki") else int(memory.rstrip("Mi")) * 1024
                cpu_usage.append(cpu_millicores)
                memory_usage.append(memory_mb)
                timestamps.append(pod["timestamp"])

        disk_io = [random.randint(1, 100) for _ in range(len(cpu_usage))]
        network_usage = [random.randint(10, 39), random.randint(30, 99)]  # [Inbound, Outbound]
        return {
            "cpuUsage": cpu_usage,
            "diskIO": disk_io,
            "memoryUsage": memory_usage,
            "networkUsage": network_usage,
            "timestamps": timestamps,
        }
    except client.exceptions.ApiException as e:
        print(f"Error fetching metrics: {e}")
        return {}


def get_applications_v2(input=None):
    namespace = "mindovermachinestech-dev"
    metrics_v1 = create_client('metrics')
    apps_v1 = create_client('apps')
    core_v1 = create_client('core')

    # Fetch deployments (representing applications)
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
    except client.exceptions.ApiException as e:
        print(f"Error fetching deployments: {e}")
        return []

    # Fetch pod metrics
    try:
        pod_metrics = metrics_v1.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )
    except client.exceptions.ApiException as e:
        print(f"Error fetching pod metrics: {e}")
        pod_metrics = {"items": []}

    # Build a dictionary of pod metrics for quick lookup
    pod_metrics_dict = {}
    for pod in pod_metrics.get("items", []):
        pod_name = pod["metadata"]["name"]
        pod_metrics_dict[pod_name] = {
            "cpu": sum(int(c["usage"]["cpu"].rstrip("n").rstrip("m")) for c in pod.get("containers", [])),
            "memory": sum(
                int(c["usage"]["memory"].rstrip("Ki").rstrip("Mi").rstrip("Gi")) for c in pod.get("containers", []))
        }

    # Generate application information
    applications = []
    for deployment in deployments.items:
        app_name = deployment.metadata.name
        app_type = "Micro Service"  # Default type; you can customize this based on labels or annotations
        registered_date = deployment.metadata.creation_timestamp.strftime("%B %d, %Y")
        status = deployment.status.available_replicas > 0 if deployment.status.available_replicas else False

        # Get memory usage for the application's pods
        memory_usage = 0
        for pod in core_v1.list_namespaced_pod(namespace=namespace).items:
            if pod.metadata.labels and pod.metadata.labels.get("app") == app_name:
                memory_usage += pod_metrics_dict.get(pod.metadata.name, {}).get("memory", 0)

        # Mock requests and activity (not available via Kubernetes API)
        requests = random.randint(200, 700)  # Mocked number of requests
        activity = f"{random.randint(1, 10)} min ago" if not status else f"{random.randint(1, 60)} sec ago"

        # Determine memory color based on usage
        memory_color = "success" if memory_usage > 30 else "warning" if memory_usage > 0 else "danger"

        # Add application details to the list
        applications.append({
            "application": {
                "name": app_name,
                "type": app_type,
                "registered": registered_date
            },
            "status": status,
            "memory": {
                "value": memory_usage,
                "period": datetime.now().strftime("%B %d, %Y"),
                "color": memory_color
            },
            "requests": str(requests),
            "activity": activity
        })

    return applications


def get_metrics():
    return {
        "cpuUsage": [random.randint(50, 99) for _ in range(15)],
        "diskIO": [random.randint(1, 100) for _ in range(15)],
        "memoryUsage": [random.randint(50, 80) for _ in range(15)],  # Memory as % Used
        "networkUsage": [random.randint(10, 39), random.randint(30, 99)],  # [Inbound, Outbound]
        "timestamps": [
            (datetime.datetime.now() - datetime.timedelta(minutes=(14 - i))).strftime("%M:%S")
            for i in range(15)
        ],
    }


def getTelemetryData():
    telemetryData = [
        {"color": "success", "title": "Load", "value": "89.9%"},
        {"color": "info", "title": "State", "value": "UP"},
        {"color": "warning", "title": "Cores", "value": "2"},
        {"color": "primary", "title": "Memory", "value": "1.95 GB"},
        {"color": "danger", "title": "All Disk", "value": "38.7 GB"},
        {"color": "dark", "title": "Up Time", "value": "2.75 years"},
    ]

    return telemetryData


def get_applications():
    applications = [
        {
            "application": {
                "name": "Inbound Kafka",
                "type": "Micro Service",
                "registered": "March 22, 2025"
            },
            "status": True,
            "memory": {
                "value": 40,
                "period": "March 22, 2025",
                "color": "success"
            },
            "requests": "420",
            "activity": "10 sec ago"
        },
        {
            "application": {
                "name": "Payment Gateway",
                "type": "API Service",
                "registered": "March 21, 2025"
            },
            "status": False,
            "memory": {
                "value": 0,
                "period": "March 21, 2025",
                "color": "danger"
            },
            "requests": "310",
            "activity": "5 min ago"
        },
        {
            "application": {
                "name": "User Authentication",
                "type": "Auth Service",
                "registered": "March 20, 2025"
            },
            "status": True,
            "memory": {
                "value": 55,
                "period": "March 20, 2025",
                "color": "warning"
            },
            "requests": "520",
            "activity": "1 min ago"
        },
        {
            "application": {
                "name": "Order Processing",
                "type": "Batch Job",
                "registered": "March 19, 2025"
            },
            "status": False,
            "memory": {
                "value": 0,
                "period": "March 19, 2025",
                "color": "danger"
            },
            "requests": "230",
            "activity": "10 min ago"
        },
        {
            "application": {
                "name": "Recommendation Engine",
                "type": "AI Model",
                "registered": "March 18, 2025"
            },
            "status": True,
            "memory": {
                "value": 30,
                "period": "March 18, 2025",
                "color": "success"
            },
            "requests": "670",
            "activity": "30 sec ago"
        }
    ]
    return applications


def get_data_center():
    data_center = {
        "metrics": get_metrics_v2(),
        "telemetryData": getTelemetryData_v2(),
        "applications": get_applications_v2(),
    }
    return data_center


def get_data_center_list():
    data_centers = [
        {
            "DC-1": [],
        },
        {
            "DC-2": [],
        },
        {
            "DC-3": [],
        }
    ]
    return data_centers


def get_system_metrics():
    return [
        {"title": "CPU Usage", "value1": 45, "value2": 85},
        {"title": "Memory Usage", "value1": 60, "value2": 92},
        {"title": "Disk I/O", "value1": 30, "value2": 70},
        {"title": "Network Bandwidth", "value1": 50, "value2": 88},
        {"title": "Active Threads", "value1": 25, "value2": 65},
        {"title": "HTTP Request Rate", "value1": 40, "value2": 75},
        {"title": "Database Query Load", "value1": 35, "value2": 80},
    ]


def get_network_metrics():
    return [
        {"title": "Network Latency", "icon": "cilSpeedometer", "value": 50, "unit": "ms"},
        {"title": "Error Rate", "icon": "cilWarning", "value": 2.3, "unit": "%"},
        {"title": "Active Database Connections", "icon": "cilLan", "value": 120, "unit": ""},
    ]


def get_performance_metrics():
    return [
        {"title": "API Success Rate", "icon": "cilCloud", "percent": 56, "value": "191,235"},
        {"title": "Service Response Time", "icon": "cilSpeedometer", "percent": 15, "value": "51,223"},
        {"title": "Database Query Performance", "icon": "cilStorage", "percent": 11, "value": "37,564"},
        {"title": "Cache Hit Ratio", "icon": "cilBolt", "percent": 8, "value": "27,319"},
    ]


def get_dash_board_metrics():
    return {
        "system_metrics": get_system_metrics(),
        "network_metrics": get_network_metrics(),
        "performance_metrics": get_performance_metrics(),
        "applications": get_applications(),
    }


# Sample Data
data_centers = {
    "DC-1": {
        "cpuUsage": [30, 45, 50, 60, 75, 80, 65, 55, 40, 30, 25, 20],
        "memoryUsage": [20, 35, 40, 55, 65, 70, 50, 40, 30, 25, 20, 10],
        "diskIO": [34, 87, 65, 23, 91, 56, 78, 45, 67, 12, 90, 43, 89, 64, 25],
        "memoryUsagePercent": 72,
        "networkUsage": [15, 48],  # [Inbound, Outbound]
        "timestamps": ["12:30", "12:31", "12:32", "12:33", "12:34", "12:35", "12:36", "12:37", "12:38", "12:39",
                       "12:40", "12:41", "12:42", "12:43", "12:44"]
    },
    "DC-2": {
        "cpuUsage": [40, 50, 60, 70, 85, 90, 75, 65, 50, 40, 35, 30],
        "memoryUsage": [30, 45, 50, 65, 75, 80, 60, 50, 40, 35, 30, 20],
        "diskIO": [45, 78, 89, 23, 56, 92, 34, 65, 87, 12, 76, 43, 59, 98, 41],
        "memoryUsagePercent": 58,
        "networkUsage": [22, 64],  # [Inbound, Outbound]
        "timestamps": ["12:30", "12:31", "12:32", "12:33", "12:34", "12:35", "12:36", "12:37", "12:38", "12:39",
                       "12:40", "12:41", "12:42", "12:43", "12:44"]
    },
    "DC-3": {
        "cpuUsage": [20, 30, 40, 50, 65, 70, 55, 45, 35, 25, 20, 15],
        "memoryUsage": [10, 25, 35, 50, 60, 65, 45, 35, 25, 20, 15, 5],
        "diskIO": [39, 67, 45, 90, 76, 54, 32, 87, 21, 65, 79, 48, 83, 92, 51],
        "memoryUsagePercent": 45,
        "networkUsage": [18, 53],  # [Inbound, Outbound]
        "timestamps": ["12:30", "12:31", "12:32", "12:33", "12:34", "12:35", "12:36", "12:37", "12:38", "12:39",
                       "12:40", "12:41", "12:42", "12:43", "12:44"]
    }
}

telemetry_data = {
    "DC-1": [
        {"color": "success", "title": "Load", "value": "89.9%"},
        {"color": "info", "title": "State", "value": "UP"},
        {"color": "warning", "title": "Cores", "value": "2"},
        {"color": "primary", "title": "Memory", "value": "1.95 GB"},
        {"color": "danger", "title": "All Disk", "value": "38.7 GB"},
        {"color": "dark", "title": "Up Time", "value": "2.75 years"},
    ],
    "DC-2": [
        {"color": "success", "title": "Load", "value": "76.3%"},
        {"color": "info", "title": "State", "value": "DOWN"},
        {"color": "warning", "title": "Cores", "value": "4"},
        {"color": "primary", "title": "Memory", "value": "3.25 GB"},
        {"color": "danger", "title": "All Disk", "value": "56.2 GB"},
        {"color": "dark", "title": "Up Time", "value": "1.45 years"},
    ],
    "DC-3": [
        {"color": "success", "title": "Load", "value": "92.5%"},
        {"color": "info", "title": "State", "value": "UP"},
        {"color": "warning", "title": "Cores", "value": "8"},
        {"color": "primary", "title": "Memory", "value": "8 GB"},
        {"color": "danger", "title": "All Disk", "value": "120 GB"},
        {"color": "dark", "title": "Up Time", "value": "5.3 years"},
    ],
}

applications = [
    {
        "application": {
            "name": "Inbound Kafka",
            "type": "Micro Service",
            "registered": "March 22, 2025"
        },
        "status": True,
        "memory": {
            "value": 40,
            "period": "March 22, 2025",
            "color": "success"
        },
        "requests": "420",
        "activity": "10 sec ago"
    },
    {
        "application": {
            "name": "Payment Gateway",
            "type": "API Service",
            "registered": "March 21, 2025"
        },
        "status": False,
        "memory": {
            "value": 0,
            "period": "March 21, 2025",
            "color": "danger"
        },
        "requests": "310",
        "activity": "5 min ago"
    },
    {
        "application": {
            "name": "User Authentication",
            "type": "Auth Service",
            "registered": "March 20, 2025"
        },
        "status": True,
        "memory": {
            "value": 55,
            "period": "March 20, 2025",
            "color": "warning"
        },
        "requests": "520",
        "activity": "1 min ago"
    },
    {
        "application": {
            "name": "Order Processing",
            "type": "Batch Job",
            "registered": "March 19, 2025"
        },
        "status": False,
        "memory": {
            "value": 0,
            "period": "March 19, 2025",
            "color": "danger"
        },
        "requests": "230",
        "activity": "10 min ago"
    },
    {
        "application": {
            "name": "Recommendation Engine",
            "type": "AI Model",
            "registered": "March 18, 2025"
        },
        "status": True,
        "memory": {
            "value": 30,
            "period": "March 18, 2025",
            "color": "success"
        },
        "requests": "670",
        "activity": "30 sec ago"
    }
]

application = {
    "applicationName": "User Management Service",
    "description": "Handles authentication, authorization, and user profile management.",
    "status": "Active",
    "owner": "John Doe",
    "version": "2.3.1",
    "hosting": "AWS ECS",
    "environment": "Production",
    "createdDate": "2023-05-10",
    "lastDeployed": "2024-03-20T14:32:00Z",
    "metrics": {
        "cpuUsage": [15, 20, 35, 50, 45, 30, 25],
        "memoryUsage": [1.2, 1.5, 2.0, 2.8, 2.5, 2.3, 1.8],
        "timestamps": ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    },
    "dependencies": [
        {
            "name": "Kafka",
            "status": "Connected"
        },
        {
            "name": "PostgreSQL",
            "status": "Connected"
        },
        {
            "name": "Redis",
            "status": "Disconnected"
        }
    ],
    "alerts": [
        {
            "time": "2024-03-20T13:45:00Z",
            "message": "High CPU usage detected",
            "severity": "Warning"
        },
        {
            "time": "2024-03-20T14:15:00Z",
            "message": "Database connection timeout",
            "severity": "Critical"
        }
    ]
}


@router.get("/datacenters")
def get_data_center_metrics():
    return get_data_center_list()


@router.get("/metrics-individual")
def get_data_center_metrics_individual():
    return get_metrics_v2()


@router.get("/telemetry-individual")
def get_data_center_metrics_individual():
    return getTelemetryData_v2()


@router.get("/applications-individual")
def get_data_center_metrics_individual():
    return get_applications_v2()


@router.get("/dashboard/metrics")
def get_dashboard_metrics():
    return get_dash_board_metrics()


@router.get("/metrics/{data_center}")
def get_data_center_metrics(data_center: str):
    """Fetch CPU and Memory usage for a specific data center."""
    if data_center in data_centers:
        return data_centers[data_center]
    return {"error": "Data center not found"}


@router.get("/telemetry/{data_center}")
def get_telemetry_data(data_center: str):
    """Fetch telemetry details for a specific data center."""
    if data_center in telemetry_data:
        return telemetry_data[data_center]
    return {"error": "Data center not found"}


@router.get("/all-metrics")
def get_all_metrics():
    """Fetch all data center metrics."""
    return data_centers


@router.get("/all-telemetry")
def get_all_telemetry():
    """Fetch telemetry data for all data centers."""
    return telemetry_data


@router.get("/applications")
def get_all_telemetry():
    """Fetch telemetry data for all data centers."""
    return applications


message = {
    "message": "Hi, Welcome to the chatbot"
}


@router.get("/message")
def get_message():
    """Fetch telemetry data for all data centers."""
    return message


@router.get("/applications_details")
def get_application_details(app_id: str):
    """Fetch application details based on app_id."""
    return get_pods_details_for_application(json.dumps({"app_name": app_id}))


def getTelemetryData_v2(namespace="mindovermachinestech-dev"):
    namespace = "mindovermachinestech-dev"
    metrics_v1 = create_client('metrics')
    apps_v1 = create_client('apps')
    core_v1 = create_client('core')

    # Fetch pod metrics for the namespace
    try:
        pod_metrics = metrics_v1.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )
    except client.exceptions.ApiException as e:
        print(f"Error fetching pod metrics: {e}")
        pod_metrics = {"items": []}

    # Aggregate pod-level metrics
    total_cpu_usage = 0
    total_memory_usage = 0
    total_pods = 0
    running_pods = 0

    for pod in pod_metrics.get("items", []):
        # Extract CPU and memory usage
        cpu_usage = sum(
            int(c["usage"]["cpu"].rstrip("n").rstrip("m")) for c in pod.get("containers", [])) / 1e9  # Convert nanocores to cores
        memory_usage = sum(
            int(c["usage"]["memory"].rstrip("Ki").rstrip("Mi").rstrip("Gi")) for c in pod.get("containers", [])) / 1024 ** 2  # Convert KiB to MiB

        # Aggregate values
        total_cpu_usage += cpu_usage
        total_memory_usage += memory_usage
        total_pods += 1

        # Check if the pod is running
        pod_name = pod["metadata"]["name"]
        try:
            pod_status = core_v1.read_namespaced_pod(name=pod_name, namespace=namespace).status.phase
            if pod_status == "Running":
                running_pods += 1
        except client.exceptions.ApiException as e:
            print(f"Error fetching pod status for {pod_name}: {e}")

    # Fetch deployments to count applications
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
        total_deployments = len(deployments.items)
    except client.exceptions.ApiException as e:
        print(f"Error fetching deployments: {e}")
        total_deployments = 0

    # Calculate load percentage
    memory_load_percentage = (total_memory_usage / (total_pods * 100)) * 100 if total_pods > 0 else 0

    # Build telemetry data
    telemetryData = [
        {
            "color": "success",
            "title": "Load",
            "value": f"{memory_load_percentage:.1f}%",
        },
        {
            "color": "info",
            "title": "State",
            "value": "UP" if running_pods > 0 else "DOWN",
        },
        {
            "color": "warning",
            "title": "Applications",
            "value": f"{total_deployments}",
        },
        {
            "color": "primary",
            "title": "Memory",
            "value": f"{total_memory_usage:.2f} GB",
        },
        {
            "color": "danger",
            "title": "Running Pods",
            "value": f"{running_pods}/{total_pods}",
        },
        {
            "color": "dark",
            "title": "Active Requests",
            "value": f"{random.randint(500, 1000)}",  # Mocked value for active requests
        },
    ]

    return telemetryData


def get_pods_details_for_application(input=None):
    print(f"invoked get_pods_and_status_health_for_application with input {input}")
    try:
        input_dict = eval(input.strip())
        # Validate if input is provided and is a dictionary
        if not isinstance(input_dict, dict):
            return "Error: 'input' must be a dictionary."

        # Validate and extract 'app_name'
        app_name = input_dict.get("app_name", "customer-service")
        if not app_name or not isinstance(app_name, str):
            return "Error: 'app_name' is required and must be a non-empty string."

        metrics_v1 = create_client('metrics')
        apps_v1 = create_client('apps')
        core_v1 = create_client('core')

        # Get pods for the specified application in 'mindovermachinestech-dev' namespace
        namespace = "mindovermachinestech-dev"
        label_selector = f"app={app_name}"
        pods = core_v1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)

        # Fetch pod metrics
        try:
            pod_metrics = metrics_v1.list_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=namespace,
                plural="pods"
            )
        except client.exceptions.ApiException as e:
            print(f"Error fetching pod metrics: {e}")
            pod_metrics = {"items": []}

        # Build a dictionary of pod metrics for quick lookup
        pod_metrics_dict = {}
        for pod in pod_metrics.get("items", []):
            pod_name = pod["metadata"]["name"]
            pod_metrics_dict[pod_name] = {
                "cpu": sum(int(c["usage"]["cpu"].rstrip("n").rstrip("m")) for c in pod.get("containers", [])),
                "memory": sum(
                    int(c["usage"]["memory"].rstrip("Ki").rstrip("Mi").rstrip("Gi")) for c in pod.get("containers", []))
            }

        pod_list = []
        for pod in pods.items:
            pod_list.append({
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "memory": pod_metrics_dict.get(pod.metadata.name, {}).get("memory", 0),
                "cpu": pod_metrics_dict.get(pod.metadata.name, {}).get("cpu", 0)
            })
        return pod_list
    except Exception as e:
        print(f"Error fetching pods: {str(e)}")
        return []
