# CNAMBOT

## Lancer le projet en local

Créez votre environnement virtuel, par exemple:

```commandline
python -m venv <your_env_name>
source <your_env_name>/bin/activate 
```

Sur Mac ou Linux, vous pouvez lancer directement le script install.sh
(qui sert normalement pour le déploiement sur GCP) :

```commandline
bash install.sh
```

Ce script installera tous les requirements python ainsi que les packages compressés contenus dans le répertoire pkg.

Pour les Windows, il suffit de lancer le script suivant dans votre terminal :

```commandline
install.bat
```

Dans le cas où cela ne fonctionne pas, lancer à la main :

```commandline
pip install -r requirements.txt
pip install pkg/*.tar.gz
```