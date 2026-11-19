# DevSecOps Personal GitHub Lab

Minimal Python HTTP app for learning GitHub Actions, SAST, DAST and container security. This repository contains no company cloud configuration or credentials.

## Step 1: Local test

```powershell
python -B app/server.py
# In another terminal:
curl.exe http://127.0.0.1:8080/healthz
```

## Step 2: Connect your own private GitHub repository

1. Create a **private** empty repository under your personal GitHub account.
2. Authenticate your workstation using Git Credential Manager or the GitHub CLI.
3. Configure origin and push:

```powershell
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/devsecops-personal-github-lab.git
git push -u origin main
```

Do not add organization-specific GKE project IDs, kubeconfig, credentials, outputs, or scans to this repository. Keep real cluster evidence offline.

## Step 3: Verify

Open GitHub -> Actions and inspect the workflow run for test/SAST/DAST. The database chapter in the playbook is documentation only; no DB operations are executed.
