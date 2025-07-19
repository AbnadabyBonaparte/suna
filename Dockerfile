# Use uma imagem base oficial do Python
FROM python:3.10-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependência para o diretêrio de trabalho
COPY requirements.txt .

# Instala as dependências do Python
# Garante que pip, setuptools e wheel estejam atualizados
# Instala as dependências do requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Define variáveis de ambiente para o Supabase (se necessário, ajuste conforme seu setup)
# ENV SUPABASE_URL="sua_url_supabase"
# ENV SUPABASE_KEY="sua_chave_supabase"

# Expõe a porta que a aplicação irá rodar (se for uma API web)
EXPOSE 8000

# Comando para iniciar a aplicação
# Se você tem um script de inicialização como \'start.py\' ou \'suna_alsham_bootstrap.py\'
# Use o comando apropriado. Exemplo:
# CMD ["python", "start.py"]
# Ou para o SUNA-ALSHAM:
CMD ["python", "suna_alsham_bootstrap.py"]
