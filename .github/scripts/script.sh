#!/bin/bash

# Autenticación (Asegúrate de que las variables de entorno o credenciales están configuradas previamente)

# Configurar el token de GitHub (usando el secret GH_TOKEN)
echo $GH_TOKEN | gh auth login --with-token 

# Configurar el token de Snyk (usando el secret SNYK_TOKEN)
snyk auth $SNYK_TOKEN

# Encabezados CSV
echo "Repo,High,Medium,Low" > vulnerabilities.csv

# Lista de repositorios (Adaptar según tus necesidades)
REPOSITORIES="centralcordoba/githubworkflowA centralcordoba/MarvelAngular"

# Bucle a través de cada repositorio
for REPO in $REPOSITORIES
do
    # Clonar el repositorio
    gh repo clone $REPO && cd $(basename $REPO)

    # Escanear con Snyk y obtener las vulnerabilidades (Puedes adaptar según tus necesidades)
    HIGH_VUL=$(snyk test --severity-threshold=high --json | jq '.uniqueCount')
    MEDIUM_VUL=$(snyk test --severity-threshold=medium --json | jq '.uniqueCount')
    LOW_VUL=$(snyk test --severity-threshold=low --json | jq '.uniqueCount')
    
    # Agregar los resultados al CSV
    echo "$REPO,$HIGH_VUL,$MEDIUM_VUL,$LOW_VUL" >> ../vulnerabilities.csv
    
    # Cambiar al directorio superior y eliminar el repo clonado (opcional)
    cd .. && rm -rf $(basename $REPO)
done
