import requests
import csv

# Tus repositorios para chequear
REPOSITORIES = [
    "centralcordoba/backendappNetCore",
    "centralcordoba/MarvelAngular"
]

# URL Base para la API de GitHub
API_URL = "https://api.github.com/repos/"

# Token de GitHub - Asegúrate de mantenerlo secreto y seguro
TOKEN = "GH_TOKEN"

# Headers para las solicitudes a la API de GitHub
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Función para obtener vulnerabilidades de un repositorio
def get_vulnerabilities(repo):
    url = f"{API_URL}{repo}/vulnerability-alerts"
    response = requests.get(url, headers=HEADERS)

    # Debug: Imprimir estado de la solicitud y respuesta
    print(f"Status Code for {repo}: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Failed to fetch vulnerabilities for {repo}.")
        return []

    # Suponiendo que la API devuelve una lista de vulnerabilidades
    vulnerabilities = response.json()
    
    # Debug: Imprimir las vulnerabilidades recibidas
    print(f"Vulnerabilities for {repo}: {vulnerabilities}")

    return vulnerabilities

# Inicializar el CSV
with open("vulnerabilities.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Repository", "Vulnerability Name", "Severity", "Package Name", "Package Version"])

    # Iterar sobre los repositorios y obtener sus vulnerabilidades
    for repo in REPOSITORIES:
        vulnerabilities = get_vulnerabilities(repo)

        # Escribir las vulnerabilidades en el CSV
        for vuln in vulnerabilities:
            try:
                writer.writerow([repo, vuln["name"], vuln["severity"], vuln["package_name"], vuln["package_version"]])
            except KeyError as e:
                # Si algún campo no existe o es diferente, imprimirlo para debug
                print(f"Error writing data for {repo}, missing key: {e}")

print("Script execution completed.")
