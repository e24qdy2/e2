# GitOps Lab: Helm and Argo CD (step-by-step)

> This is a public, generic education example. There are no company cluster names, credentials or internal networking details in this repository.

## 1. Verified: CI and release
- CI: smoke tests, Semgrep source scan, ZAP baseline.
- CodeQL: Python and workflow static analysis.
- Container: Docker build, Trivy HIGH/CRITICAL gate, then publish to GHCR only if scan succeeds.
- Helm source: `helm/e2-demo`. Keep the image pinned to an immutable commit SHA; never silently deploy `latest`.

## 2. Verify a chart without a Kubernetes cluster
```powershell
helm lint .\helm\e2-demo
helm template e2-demo .\helm\e2-demo --namespace default
```
This checks YAML rendering only. It does not install anything.

## 3. Helm deployment
On an **authorized sandbox Kubernetes context** with enough free capacity and namespace-scoped RBAC, use an isolated namespace and explicit context:
```powershell
helm upgrade --install e2-demo .\helm\e2-demo --namespace YOUR_SANDBOX_NS --kube-context YOUR_SANDBOX_CONTEXT --wait
kubectl --context YOUR_SANDBOX_CONTEXT -n YOUR_SANDBOX_NS rollout status deployment/lab-http
```
If an existing Deployment with the same name is already managed by kubectl or another Helm release, stop and agree on ownership migration before running the command. Do not use `--force-conflicts` or `--take-ownership` routinely.

For a new standalone namespace without pre-created resources, set `serviceAccount.create=true,service.enabled=true` in environment-specific private values.

## 4. Argo CD — learn the reconciliation model
Git source -> Argo CD Application -> destination Kubernetes cluster.
- `repoURL`: https://github.com/e24qdy2/e2.git
- `path`: helm/e2-demo
- `targetRevision`: pin a tested Git ref; avoid mutable HEAD for promoted releases
- `destination`: cluster registered with Argo CD, namespace scoped to the lab
- `syncPolicy`: start with **manual sync** and inspect Diff; enable self-heal only after controlled tests

Argo CD needs access to both GitHub and the Kubernetes API of the destination. A private Kubernetes API must be reachable from the management-plane network and mapped to a narrow service account / cluster role binding.

## 5. Do not mix controllers
The same Deployment should not be independently managed by Helm CLI and Argo CD at the same time.
For a transition, back up Helm release state and object manifests, test Argo Diff, then execute an authorized ownership handover. Never uninstall a Helm release blindly if that would delete the live Deployment.

## 6. Not performed in this lab
- Installing Argo CD on shared company GKE nodes
- Registering corporate GKE as an Argo CD target
- Automatic sync/rollback to corporate workloads
- Database creation, migration, or any SQL execution

See `docs/database-devops.md` for the read-only DB migration chapter.
