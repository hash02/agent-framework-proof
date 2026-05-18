# Kubernetes Mini Deploy

This folder contains a local Kubernetes proof for the FastAPI service.

It is designed for kind, minikube, Docker Desktop Kubernetes, or another local cluster. It is not a production EKS claim.

## What It Proves

- The service can be described as a Kubernetes workload.
- The container has a repeatable port and health endpoint.
- The deployment includes readiness and liveness probes.
- The service has a stable in-cluster selector.
- The manifests can be validated by tests before being discussed in a resume or packet.

## Files

- `deployment.yaml`: single-replica deployment for the FastAPI proof service.
- `service.yaml`: ClusterIP service exposing port 8000.
- `kustomization.yaml`: local apply target.

## Local Commands

Build the image:

```powershell
docker build -t agent-framework-proof:local .
```

Apply to a local cluster:

```powershell
kubectl apply -k k8s
```

Check rollout:

```powershell
kubectl rollout status deployment/agent-framework-proof
kubectl get pods -l app=agent-framework-proof
```

Port forward:

```powershell
kubectl port-forward service/agent-framework-proof 8000:8000
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

## Boundary

This is a local deployment artifact only. Do not describe it as production Kubernetes, EKS, Terraform, ArgoCD, or cloud ownership.
