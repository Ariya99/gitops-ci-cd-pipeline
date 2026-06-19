# gitops-ci-cd-pipeline

Production-grade GitOps CI/CD reference implementation demonstrating enterprise Kubernetes deployment maturity.

**Author:** [Ariya99](https://github.com/Ariya99)
![CI](https://github.com/Ariya99/gitops-ci-cd-pipeline/actions/workflows/ci.yml/badge.svg)
## Architecture

```
Developer → Git Push → GitHub Actions (CI)
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
                 Tests     SAST      Lint
                    │         │         │
                    └─────────┼─────────┘
                              ▼
                    Docker Build → Trivy Scan
                              ▼
                    Push to GHCR (immutable SHA tag)
                              ▼
                    Update GitOps values (image tag)
                              ▼
                    ArgoCD Sync (auto + self-heal)
                              ▼
                    Helm Deploy → Kubernetes
                              ▼
              Argo Rollouts Canary (staging/prod)
                              ▼
              Prometheus Metrics + Grafana Dashboard
                              │
                    failure? ─┴─► Auto Rollback Loop
```

### Flow

1. **Developer** pushes code to `main`
2. **GitHub Actions** runs tests, lint, SAST (Bandit), builds Docker image
3. **Trivy** scans the image for CRITICAL/HIGH vulnerabilities
4. Image pushed to **GHCR** with immutable tag (`git SHA`)
5. CI commits updated image tags to `gitops-infra/values-*.yaml`
6. **ArgoCD** detects drift, syncs Helm chart to cluster
7. **Argo Rollouts** performs canary deployment with gradual traffic shift
8. **Prometheus** monitors success/error rates during canary analysis
9. On failure → automatic rollback via Rollouts analysis or manual via ArgoCD/Helm/kubectl

## Repository Structure

```
gitops-ci-cd-pipeline/
├── app/                          # Application source
│   ├── src/                      # FastAPI app with /metrics endpoint
│   ├── tests/                    # Unit tests
│   ├── Dockerfile                # Multi-stage, non-root
│   └── .github/workflows/ci.yml  # CI reference (active: root .github/)
├── gitops-infra/                 # GitOps configuration
│   ├── helm/chart/               # Helm chart (Deployment or Rollout)
│   ├── values-dev.yaml           # Dev environment overrides
│   ├── values-staging.yaml       # Staging + canary enabled
│   ├── values-prod.yaml          # Production + HPA + strict canary
│   ├── argo-apps/                # ArgoCD Application manifests
│   ├── rollouts/                 # Canary analysis templates
│   ├── observability/            # Prometheus rules + Grafana dashboard
│   ├── policies/                 # OPA Gatekeeper constraints
│   └── rollback.md               # Rollback runbook
└── .github/workflows/ci.yml      # Active CI pipeline
```

## Prerequisites

| Component | Purpose |
|-----------|---------|
| Kubernetes 1.28+ | Runtime platform |
| ArgoCD | GitOps continuous delivery |
| Argo Rollouts | Progressive delivery |
| Helm 3 | Package management |
| Prometheus Operator | Metrics collection |
| Gatekeeper | Policy enforcement |
| NGINX Ingress | Traffic routing for canary |

## Quick Start

### 1. Bootstrap ArgoCD Applications

```bash
kubectl apply -f gitops-infra/argo-apps/dev.yaml
kubectl apply -f gitops-infra/argo-apps/staging.yaml
kubectl apply -f gitops-infra/argo-apps/prod.yaml
```

### 2. Apply Observability & Policies

```bash
kubectl apply -f gitops-infra/observability/prometheus/
kubectl apply -f gitops-infra/observability/grafana/
kubectl apply -f gitops-infra/policies/
kubectl apply -f gitops-infra/rollouts/canary.yaml
```

### 3. Configure GitHub

- Enable **GitHub Packages** (GHCR) for the repository
- Grant `GITHUB_TOKEN` write permissions for contents (Settings → Actions → General)
- Optional: create `GITOPS_PAT` if using a separate GitOps repository

### 4. Local Development

```bash
cd app
pip install -r requirements-dev.txt
pytest tests/ -v
uvicorn src.main:app --reload --port 8080
```

## CI Pipeline

| Stage | Tool | Gate |
|-------|------|------|
| Lint | Ruff | Must pass |
| SAST | Bandit | Must pass |
| Unit Tests | Pytest | Must pass |
| Build | Docker Buildx | — |
| Scan | Trivy | CRITICAL/HIGH block |
| Push | GHCR | Immutable SHA tag |
| GitOps Update | sed + git commit | Auto on main |

## CD Pipeline

| Environment | Namespace | Rollout | Replicas | Notes |
|-------------|-----------|---------|----------|-------|
| dev | app-dev | Deployment | 1 | Fast iteration |
| staging | app-staging | Canary | 2 | Canary validation |
| prod | app-prod | Canary | 3+ | HPA, TLS, strict analysis |

ArgoCD sync policy: **automated**, **prune**, **selfHeal**, **CreateNamespace**.

## Progressive Delivery

Staging and production use **Argo Rollouts canary** strategy:

```
10% → pause 3m → 30% → pause 3m → 60% → pause 3m → 100%
```

Prometheus analysis runs during each pause. If success rate drops below threshold, Rollouts automatically aborts and rolls back.

## Rollback Strategies

See [gitops-infra/rollback.md](gitops-infra/rollback.md) for the full runbook.

| Method | Command | When |
|--------|---------|------|
| Argo Rollouts | `kubectl argo rollouts undo gitops-app -n app-prod` | Canary failure |
| ArgoCD | `argocd app rollback gitops-app-prod` | Bad GitOps commit |
| Helm | `helm rollback gitops-app <rev> -n app-prod` | Release-level revert |
| kubectl | `kubectl rollout undo deployment/gitops-app` | Emergency (dev) |

## Security Practices

- Non-root container user (UID 1000)
- `readOnlyRootFilesystem`, drop all capabilities
- `seccompProfile: RuntimeDefault`
- Trivy image scanning in CI (fail on CRITICAL/HIGH)
- Bandit SAST for Python source
- Gatekeeper policies: deny privileged containers, require standard labels
- Immutable image tags (git SHA, never floating tags in prod values after CI)

## Observability

- App exposes `/metrics` (Prometheus format)
- `ServiceMonitor` for auto-discovery
- `PrometheusRule` alerts: high error rate, target down, high latency
- Grafana dashboard ConfigMap with request rate, error rate, pod restarts

## Draw.io Diagram Export

Use this node/edge list for diagram generation:

```
Nodes:
  - Developer
  - GitHub (Repository)
  - GitHub Actions (CI)
  - GHCR (Container Registry)
  - GitOps Repo (values-*.yaml)
  - ArgoCD
  - Kubernetes Cluster
  - Argo Rollouts (Canary)
  - Prometheus
  - Grafana
  - Rollback Loop

Edges (directed):
  Developer → GitHub → GitHub Actions
  GitHub Actions → GHCR (build + push)
  GitHub Actions → GitOps Repo (update image tag)
  GitOps Repo → ArgoCD (watch)
  ArgoCD → Kubernetes (helm sync)
  Kubernetes → Argo Rollouts (canary traffic shift)
  Argo Rollouts → Prometheus (analysis queries)
  Prometheus → Grafana (dashboards)
  Prometheus → Rollback Loop (analysis failure)
  Rollback Loop → Argo Rollouts (abort/undo)
  Rollback Loop → ArgoCD (git revert)
```

## License

MIT
