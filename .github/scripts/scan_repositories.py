import requests
import csv

# Token de GitHub para autenticación
GITHUB_TOKEN = "GH_TOKEN"

# Lista de repositorios a comprobar
REPOSITORIES = ["centralcordoba/githubworkflowA", "centralcordoba/MarvelAngular"]

# URL de la API de GitHub para solicitar las vulnerabilidades
API_URL_TEMPLATE = "https://api.github.com/repos/{}/vulnerability-alerts"

# Headers para la solicitud a la API de GitHub
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Inicializar un archivo CSV para registrar las vulnerabilidades
with open("vulnerabilities.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Repository", "Vulnerability Name", "Severity", "Package Name", "Package Version"])

    # Iterar a través de cada repositorio y registrar las vulnerabilidades en el CSV
    for repo in REPOSITORIES:
        response = requests.get(API_URL_TEMPLATE.format(repo), headers=HEADERS)
        
        # Gestión de errores básica para la respuesta de la API
        if response.status_code == 200:
            vulnerabilities = response.json()
            for vuln in vulnerabilities:
                writer.writerow([
                    repo,
                    vuln["name"],
                    vuln["severity"],
                    vuln["package_name"],
                    vuln["package_version"],
                ])
        else:
            print(f"Error fetching data for {repo}: {response.status_code}")
