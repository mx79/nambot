# CNAMBOT

## Lancer le projet en local

Lancer les commandes suivantes dans votre terminal,
cela créera votre environnement virtuel puis y installera
les packages requis pour faire tourner le projet:

```commandline
python -m venv <your_env_name>
source <your_env_name>/bin/activate 
pip install -r requirements.txt
```

Cependant, vous devez garder à l'esprit que vous faire tourner le site en local,
il vous faudra accès aux variables d'environnements nécessaires.

Il y a par exemple: le cluster Mongo, il vous faut demander la création d'un identifiant
par l'admin de CnamBot afin de pouvoir requêter la base et faire des tests.

Ainsi que toutes les autres variables de configuration du projet comme le type de session utlisée, etc.

## Le déploiement

Plusieurs sites différents seront sans doute testés pour le déploiement du site CnamBot.

Nous commencerons sans doute par Google Cloud Platform (GCP).

Le cas échéant, la documentation à titre de repère sera inscrite dans cette section.

### GCP (coming soon...)