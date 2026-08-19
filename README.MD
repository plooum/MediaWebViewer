# Media Web Viewer - Documentation & Guide

Une application web développée avec **Flask** et **Gunicorn** pour visualiser et télécharger des fichiers multimédias (images et vidéos).
L'implémentation et le design actuel m'ont permis de partager mes photos et vidéos de l'éclipse solaire du 12 aout 2026 🌒.

---

## 🛠️ Description du Script (`app.py`)

Le fichier `app.py` est une application web auto-contenue en Python basée sur le framework **Flask**. 

### 🌟 Fonctionnalités Principales :
* 📂 **Scan Automatique** : Balaye le répertoire `./media` à la recherche de fichiers multimédias.
* 📸 **Support Multi-Format** :
  * **Images** : `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`
  * **Vidéos** : `.mp4`, `.webm`, `.ogg`, `.mov`, `.mkv`
* 🖼️ **Interface Modernised avec Lightbox** :
  * Thème sombre sombre et épuré (*Cloudy Eclipse Theme*).
  * Modal/Lightbox interactif permettant d'agrandir et visualiser les images en grand écran.
  * Gestion du clavier (touche `Échap` pour fermer).
* ⬇️ **Téléchargement Dédié** :
  * Bouton de téléchargement direct pour chaque fichier.
  * Route dynamique `/download-all` : Génère à la volée une archive `all.zip` contenant l'ensemble des médias si celle-ci n'existe pas déjà.

---

## ⚙️ Structure du Fichier `Dockerfile`

Le fichier `Dockerfile` permet d'encapsuler l'application dans un conteneur standardisé et prêt pour la production.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY app.py .
RUN mkdir media

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

* **Base Image** : Utilise `python:3.11-slim` pour réduire la taille globale de l'image.
* **Serveur de Production** : Installe et utilise **Gunicorn** avec 4 *workers* configurés.
* **Port d'Écoute** : Le serveur Gunicorn écoute en interne sur le port `5001`.

---

## 🚀 Exploitation & Déploiement avec Docker

Suivez ces étapes simples pour construire et exécuter le projet sur votre environnement Docker.

### 📋 1. Organisation des Fichiers
Assurez-vous que vos fichiers sont organisés comme suit :

```text
project-folder/
├── app.py
├── Dockerfile
└── README.md
```

### 🏗️ 2. Construction de l'Image Docker
Exécutez la commande suivante dans le terminal pour construire l'image conteneurisée :

```bash
docker build -t eclipse-gallery .
```

### ▶️ 3. Lancement du Conteneur

Le serveur Gunicorn dans le conteneur écoute sur le port **5001**. Vous devez mapper ce port vers un port hôte de votre choix (par exemple, le port `8080`).

#### 🔹 Option A : Lancement standard (Dossier vidéo/image interne)
```bash
docker run -d -p 8080:5001 --name eclipse-media-server eclipse-gallery
```

#### 🔹 Option B : Lancement avec Persistance / Montage de Répertoire Local (Recommandé)
Pour afficher directement vos propres fichiers situés dans un dossier de votre machine locale sans modifier le conteneur, utilisez un volume :

```bash
docker run -d \
  -p 8080:5001 \
  -v /chemin/vers/vos/medias:/app/media \
  --name eclipse-media-server \
  eclipse-gallery
```

---

## 🌐 Accès à l'Application

Une fois le conteneur démarré, ouvrez votre navigateur et accédez à :

👉 **`http://localhost:8080`**

---

## 🧹 Commandes Utiles

* **Consulter les logs** :
  ```bash
  docker logs -f eclipse-media-server
  ```
* **Arrêter le conteneur** :
  ```bash
  docker stop eclipse-media-server
  ```
* **Supprimer le conteneur** :
  ```bash
  docker rm eclipse-media-server
