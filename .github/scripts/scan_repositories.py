import os
import requests
import pandas as pd

# Definir constantes
GITHUB_TOKEN = os.getenv('GH_TOKEN')  # Asegúrate de configurar este secreto en tu GitHub Actions
REPOSITORIES = ["repo_owner/repo1", "repo_owner/repo2"]  # Lista de repositorios a verificar
API_URL_TEMPLATE = "https://api.github.com/repos/{}/vulnerability-alerts"

# Configurar encabezados de solicitud
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Dataframe para almacenar datos de vulnerabilidad
vulnerabilities_df = pd.DataFrame(columns=["Repo", "Vulnerability", "Severity"])

# Iterar sobre cada repositorio
for repo in REPOSITORIES:
    # Solicitar datos de vulnerabilidades del repositorio
    response = requests.get(API_URL_TEMPLATE.format(repo), headers=HEADERS)
    
    if response.status_code == 200:
        vulnerabilities = response.json()
        
        # Extraer y almacenar datos de vulnerabilidad
        for vuln in vulnerabilities:
            vulnerabilities_df = vulnerabilities_df.append({
                "Repo": repo,
                "Vulnerability": vuln.get("name", ""),
                "Severity": vuln.get("severity", "")
            }, ignore_index=True)
    
    else:
        print(f"Failed to fetch vulnerabilities for {repo}: {response.status_code}")
    
# Guardar datos en un archivo CSV
vulnerabilities_df.to_csv("vulnerabilities.csv", index=False)
