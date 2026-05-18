from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
K8S = ROOT / "k8s"


def read_manifest(name: str) -> str:
    return (K8S / name).read_text(encoding="utf-8")


def test_deployment_manifest_has_health_probes_and_limits():
    text = read_manifest("deployment.yaml")

    assert "kind: Deployment" in text
    assert "name: agent-framework-proof" in text
    assert "image: agent-framework-proof:local" in text
    assert "containerPort: 8000" in text
    assert "readinessProbe:" in text
    assert "livenessProbe:" in text
    assert "path: /health" in text
    assert "resources:" in text
    assert "limits:" in text


def test_service_manifest_selects_app_and_exposes_http_port():
    text = read_manifest("service.yaml")

    assert "kind: Service" in text
    assert "type: ClusterIP" in text
    assert "app: agent-framework-proof" in text
    assert "port: 8000" in text
    assert "targetPort: http" in text


def test_kustomization_references_all_manifests():
    text = read_manifest("kustomization.yaml")

    assert "deployment.yaml" in text
    assert "service.yaml" in text
