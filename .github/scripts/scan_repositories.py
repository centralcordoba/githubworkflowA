import requests
import pandas as pd
import os

# Reemplazar con tu token de GitHub
TOKEN = 'GH_TOKEN'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.vixen-preview+json'
}

# Lista de repositorios para verificar
REPOS = [
    {'owner': 'centralcordoba', 'repo': 'githubworkflowA'},
    {'owner': 'centralcordoba', 'repo': 'MarvelAngular'},
    # Añadir más repositorios si es necesario
]

# Lista para almacenar los datos recopilados
data = []

# Iterar sobre cada repositorio y obtener las alertas de seguridad
for repo_info in REPOS:
    owner = repo_info['owner']
    repo = repo_info['repo']
    url = f'https://api.github.com/repos/{owner}/{repo}/vulnerability-alerts'
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        vulnerabilities = response.json()
        
        for vuln in vulnerabilities:
            data.append({
                'Repository': f"{owner}/{repo}",
                'Vulnerability': vuln['security_advisory']['vulnerabilities'][0]['package']['name'],
                'Severity': vuln['security_advisory']['vulnerabilities'][0]['severity'],
                'Updated_At': vuln['security_advisory']['updated_at'],
                'Advisory_URL': vuln['security_advisory']['html_url']
            })
    elif response.status_code == 404:
        print(f"No vulnerabilities found for {owner}/{repo}.")
    else:
        print(f"Failed to fetch vulnerabilities for {owner}/{repo}.")

# Convertir los datos a un DataFrame y luego a un CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv('vulnerabilities.csv', index=False)
    print("CSV file created successfully.")
else:
    print("No vulnerabilities found for all repositories.")
