import requests
import csv
import os

# Obtener el token de GitHub desde las variables de entorno
TOKEN = os.getenv("GH_TOKEN")

# Verificación del token
if TOKEN is None:
    raise ValueError("GH_TOKEN no está definido.")

# Configuración del encabezado para las solicitudes HTTP
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.vixen-preview+json"
}

# Repositorios a verificar
REPOSITORIES = [
    "centralcordoba/githubworkflowA",
    "centralcordoba/MarvelAngular",
    # Añadir más repositorios según sea necesario
]

# Inicializar el archivo CSV
with open('vulnerabilities.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Repository", "Vulnerability Name", "Severity", "Package Name", "Package Version"])
    
    # Loop a través de cada repositorio
    for repo in REPOSITORIES:
        print(f"Fetching vulnerabilities for {repo}...")
        url = f"https://api.github.com/repos/{repo}/vulnerability-alerts"
        
        # Realizar la solicitud HTTP
        response = requests.get(url, headers=HEADERS)
        
        # Verificación de la respuesta
        if response.status_code != 200:
            print(f"Status Code for {repo}: {response.status_code}")
            print("Failed to fetch vulnerabilities. Response Headers:")
            print(response.headers)
            print("Response Body:")
            print(response.text)
            continue
        
        # Procesar la respuesta JSON
        vulnerabilities = response.json()
        for vuln in vulnerabilities:
            writer.writerow([
                repo,
                vuln.get('name', ''),
                vuln.get('severity', ''),
                vuln.get('vulnerable_package_name', ''),
                vuln.get('vulnerable_package_version', '')
            ])
        
        print(f"Vulnerabilities for {repo} fetched and recorded.")

print("Script execution completed.")
