import os
import requests
import csv

# URL base de la API de GitHub para obtener las vulnerabilidades
VULNERABILITIES_URL = "https://api.github.com/repos/{}/vulnerability-alerts"

# Repositorios a analizar
REPOSITORIES = [
    "centralcordoba/githubworkflowA",
    "centralcordoba/MarvelAngular",
    # ... otros repositorios ...
]

# Token de acceso personal de GitHub
TOKEN = os.getenv("GH_TOKEN")

# Encabezados de la solicitud HTTP
HEADERS = {
    "Accept": "application/vnd.github.vixen-preview+json",
    "Authorization": f"token {TOKEN}"
}

# Nombre del archivo CSV donde se guardarán los resultados
CSV_FILENAME = "vulnerabilities.csv"

def fetch_vulnerabilities(repo):
    """
    Fetch the vulnerabilities for the given repo using GitHub API.
    
    Parameters:
        repo (str): The repository in the form "owner/repo".
    
    Returns:
        dict: The JSON response from the API if successful, otherwise None.
    """
    response = requests.get(VULNERABILITIES_URL.format(repo), headers=HEADERS)
    
    if response.status_code == 204:
        print(f"No vulnerabilities found for {repo}.")
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch vulnerabilities for {repo}.")
        print(f"Status Code for {repo}: {response.status_code}")
        print(f"Response Headers:\n{response.headers}")
        print(f"Response Body:\n{response.text}")
        return None

def main():
    """
    Main function that fetches vulnerabilities for repositories and saves them to a CSV file.
    """
    with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir encabezados de columna
        writer.writerow(["Repository", "Vulnerability Name", "Severity", "Package Name", "Package Version"])
        
        for repo in REPOSITORIES:
            print(f"Fetching vulnerabilities for {repo}...")
            vulnerabilities = fetch_vulnerabilities(repo)
            
            # Procesar las vulnerabilidades si las hay
            if vulnerabilities:
                for vuln in vulnerabilities:
                    writer.writerow([
                        repo,
                        vuln['security_advisory']['ghsa_id'],
                        vuln['security_advisory']['severity'],
                        vuln['vulnerable_package_name'],
                        vuln['vulnerable_package_version']
                    ])

# Si este script se ejecuta como el principal, ejecutar la función principal
if __name__ == "__main__":
    main()
