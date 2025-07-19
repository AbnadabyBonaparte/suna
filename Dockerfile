# Use uma imagem base oficial do Python
FROM python:3.10-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependência para o diretêrio de trabalho
COPY requirements.txt .

# Instala as dependências do Python
# Garante que pip, setuptools e wheel estejam atualizados
# Instala as dependências do requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools==65.5.1 wheel==0.41.0 \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "suna_alsham_bootstrap.py"]
