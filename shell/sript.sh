#!/bin/bash

# Verifica se o arquivo de log foi fornecido como argumento
if [ $# -eq 0 ]; then
  echo "Por favor, forneça o caminho para o arquivo de log como argumento."
  exit 1
fi

# Extrai todos os IPs únicos do arquivo de log
awk -F';' '{print $2}' $1 | sort -u