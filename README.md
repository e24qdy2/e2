# DevSecOps e2 — Public Learning Repository

Small **independent demo application** for learning GitHub Actions, CodeQL, Semgrep, OWASP ZAP, container image security, and GHCR publication. Do not use this repository to store company GKE configuration, credentials, internal endpoints, billing data, or enterprise security evidence.

## Completed CI stages
- **CI DevSecOps Starter**: syntax check, HTTP smoke tests, Semgrep SAST and OWASP ZAP baseline against the app running on **localhost inside GitHub Actions**.
- **CodeQL Advanced**: analysis of Python and GitHub Actions.
- **Container Build, Trivy Gate and GHCR**: builds Docker image, generates JSON CVE evidence, fails the pipeline on any HIGH/CRITICAL finding, and publishes the image to GHCR **only when the security gate passes**.

## Actions step-by-step
1. Open [Actions](https://github.com/e24qdy2/e2/actions).
2. Check `CI DevSecOps Starter`, `CodeQL Advanced`, and `Container Build, Trivy Gate and GHCR`.
3. For container security, download the **trivy-image-report** artifact and inspect findings.
4. If HIGH/CRITICAL CVEs are reported, fix them in a Pull Request and wait for a green Trivy gate before releasing.
5. If all checks pass on a push to `main`, verify the pushed image under GitHub **Packages**. Images are tagged with the Git commit SHA.

## Local run
```bash
python -B app/server.py
# In another terminal:
curl -i http://127.0.0.1:8080/healthz
```

```bash
docker build --pull -t e2-lab:local .
docker run --rm -p 127.0.0.1:8080:8080 e2-lab:local
```

## Database DevOps
Read `docs/database-devops.md` for Flyway and DBA-approval concepts. This is **documentation only**: no workflow creates or modifies a database.

## Separation and safety
This demo **does not deploy to corporate GKE**. It uses a GitHub-hosted runner and local HTTP preview only. Never add kubeconfig, service account keys, production data, vulnerability reports from company systems, or internal identifiers to this public repository.

This demonstration does not certify the application as production secure; the scanners have limited coverage and require review of their findings.
