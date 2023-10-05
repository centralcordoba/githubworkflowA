import requests
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Token de autenticación para la API de GitHub
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.vixen-preview+json",
    "Authorization": f"token {TOKEN}"
}

# Lista de repositorios a verificar
REPOSITORIES = ["centralcordoba/githubworkflowA", "centralcordoba/MarvelAngular"]

def fetch_vulnerabilities(repo):
    logging.info(f"Fetching vulnerabilities for {repo}...")
    url = f"https://api.github.com/repos/{repo}/vulnerability-alerts"
    response = requests.get(url, headers=HEADERS)

    logging.info(f"Status Code for {repo}: {response.status_code}")
    
    if response.status_code == 204:
        logging.info(f"No vulnerabilities found for {repo}.")
        return []
    elif response.status_code != 200:
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
    for repo in REPOSITORIES:
        vulnerabilities = fetch_vulnerabilities(repo)
        all_vulnerabilities.extend(vulnerabilities)
    
    if not all_vulnerabilities:
        logging.info("No vulnerabilities found for all repositories.")
        return
    
    # Aquí puedes añadir lógica para procesar/exportar las vulnerabilidades, por ejemplo, guardarlas en un archivo CSV.
    logging.info("Vulnerabilities found:")
    for vuln in all_vulnerabilities:
        logging.info(f"{vuln['Repository']}: {vuln['Vulnerability Name']} ({vuln['Severity']}) in {vuln['Package Name']} {vuln['Package Version']}")

if __name__ == "__main__":
    main()
