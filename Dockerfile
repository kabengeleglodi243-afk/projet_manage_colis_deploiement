FROM python:3.12-slim 
# Variables Python 
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 
# Répertoire de travail 
WORKDIR /app 
# Copier requirements 
COPY requirements.txt . 
# Installer les dépendances Python 
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 
# Copier le projet 
COPY ./ /app 