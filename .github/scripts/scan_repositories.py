import requests
import pandas as pd
import os

# Import logging
import logging

logging.basicConfig(level=logging.INFO)

# Tu token personal de GitHub
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.vixen-preview+json"
}

# Lista de repositorios a verificar
REPO_LIST = [
    'centralcordoba/githubworkflowA',
    'centralcordoba/MarvelAngular',
    # Agrega los repositorios adicionales aquí
]

def fetch_vulnerabilities(repo):
    logging.info(f"Fetching vulnerabilities for {repo}...")
    url = f"https://api.github.com/repos/{repo}/vulnerability-alerts"
    response = requests.get(url, headers=HEADERS)

    logging.info(f"Status Code for {repo}: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Failed to fetch vulnerabilities for {repo}.")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        return []

    vulnerabilities = response.json()
    logging.info(f"Found {len(vulnerabilities)} vulnerabilities for {repo}.")
    return [
        {
            "Repository": repo,
            "Vulnerability Name": vuln["security_advisory"]["vulnerabilities"][0]["package"]["name"],
            "Severity": vuln["security_advisory"]["severity"],
            "Package Name": vuln["security_advisory"]["vulnerabilities"][0]["package"]["name"],
            "Package Version": vuln["security_advisory"]["vulnerabilities"][0]["version"]
        }
        for vuln in vulnerabilities
    ]

def main():
    all_vulnerabilities = []

    for repo in REPO_LIST:
        vulnerabilities = fetch_vulnerabilities(repo)
        all_vulnerabilities.extend(vulnerabilities)

    if all_vulnerabilities:
        df = pd.DataFrame(all_vulnerabilities)
        df.to_csv("vulnerabilities.csv", index=False)
        logging.info("CSV file with vulnerabilities created successfully.")
    else:
        logging.info("No vulnerabilities found for all repositories.")

if __name__ == "__main__":
    main()
