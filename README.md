# Kubernetes for Modern Data Engineering


This repository contains a local Kubernetes setup for running Apache Airflow using Docker Desktop, Helm, and git-sync. The project includes both Airflow DAGs and the necessary Kubernetes configuration to deploy Airflow and the Kubernetes Dashboard locally — without relying on any cloud provider.

🔗 **Medium Blog post:** [Kubernetes for Modern Data Engineering](https://medium.com/@dominikzygarski_88070/project-kubernetes-for-modern-data-engineering-7e1d6b49e56a)


## ⚙️ Tech Stack

- Kubernetes (via Docker Desktop)
- Apache Airflow (via Helm)
- gitSync
- Python


## 📁 Repository Structure

```
.
├── dags/
│   ├── fetch_and_preview.py       # Data workflow using PythonOperator + pandas
│   └── hello.py                   # Basic example DAG
└── k8s/
    ├── dashboard-adminuser.yaml   # Admin user for Kubernetes Dashboard
    ├── dashboard-clusterrole.yaml # RBAC role config
    ├── dashboard-secret.yaml      # Login token config
    └── values.yaml                # Airflow Helm config (executor, logging, gitSync, etc.)
```

## 🧰 Prerequisites

- Docker Desktop with Kubernetes enabled  
- `kubectl` and `helm` installed

## 🛠 Setup

### Deploy the Kubernetes Dashboard

To deploy the Kubernetes Dashboard locally with proper access configuration:

```bash
kubectl apply -f k8s/
```

This applies all required YAML files for RBAC, admin user, and secrets. It will configure a working dashboard accessible from your machine.


### Access the Dashboard

Start a proxy server:

```bash
kubectl proxy
```

Then open:

[http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/)

To log in, use the token defined in `dashboard-secret.yaml`. Retrieve it with:

```bash
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 --decode
```


### Deploy Apache Airflow

Make sure you’ve added the Airflow Helm repository:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

Then deploy Airflow using the configuration file provided:

```bash
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  -f k8s/values.yaml
```

This will install Airflow with `KubernetesExecutor`, enabled `git-sync`, and persistent logging.


### DAG Management with Git-Sync

You don’t need to manually copy DAGs into the container.

This project uses **git-sync**, which automatically pulls DAGs from the `main` branch of your GitHub repository. The `subPath: "dags"` ensures only DAG files from that folder are loaded.

After pushing new or updated DAGs to GitHub, Airflow will detect and load them automatically — no restart required.



## 🙏 Acknowledgements

The structure and direction of this project follow the approach shared by [airscholar](https://github.com/airscholar).
