# Lab 16: Release approval and promotion (safe read-only demo)

Workflow: .github/workflows/manual-release-approval.yml

1. GitHub Actions -> Lab 16 - Manual Release Approval -> Run workflow.
2. Enter the exact commit SHA corresponding to a tested GHCR image.
3. The job checks that CI DevSecOps Starter, CodeQL Advanced, and Container Build/Trivy/GHCR completed successfully for the same SHA.
4. The job verifies Helm rendering for that immutable tag.
5. Configure the GitHub environment **lab-release-approval** under Settings > Environments. Add required reviewers where supported and available. A manually triggered workflow alone is NOT a human reviewer approval rule.
6. This lab job does NOT deploy to Kubernetes, change branch protection or publish an image.

In production use protected branches, two-person review, environment approval and a separate trusted deployment identity. Never put company GKE credentials into this public lab.
