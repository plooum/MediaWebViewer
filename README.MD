
readme_content = """# 🌒 Solar Eclipse Media Gallery - Documentation & Guide

Une application web moderne, légère et élégante développée avec **Flask** et **Gunicorn** pour visualiser et télécharger des fichiers multimédias (images et vidéos) d'un événement céleste (ex: Éclipse Solaire).

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