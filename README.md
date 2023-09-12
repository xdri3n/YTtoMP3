# YoutubeToMP3

Un outil pour télécharger des vidéos YouTube et les convertir en MP3 avec des métadonnées et des images d'album.

## Prérequis

- Python 3
- Les bibliothèques Python suivantes : `yt_dlp`, `pydub`, `requests`, `eyed3`, `csv`
- FFmpeg

## Utilisation

### Télécharger depuis un fichier CSV

1. Remplissez votre fichier CSV avec les colonnes `url`, `artist`, et `title`.
2. Exécutez la commande suivante :

### Sans préciser le csv
```bash
python3 youtube_to_mp3.py
```

### En précisant le csv
```bash
python3 youtube_to_mp3.py --csv "CHEMIN_VERS_LE_CSV"
```

Par défaut, les fichiers seront enregistrés dans le dossier ./output avec un bitrate de 128k. Vous pouvez modifier ces valeurs avec les arguments --output_folder et --bitrate.

## Télécharger depuis une URL

Si vous souhaitez télécharger une seule vidéo sans utiliser un fichier CSV, utilisez la commande suivante :

```bash
python3 youtube_to_mp3.py --url "URL_DE_LA_VIDEO" --title "TITRE" --artist "ARTISTE" --output_folder "DOSSIER_DE_SORTIE" --bitrate "BITRATE"
```

## Options

- --csv: Chemin vers le fichier CSV contenant les vidéos à télécharger.
- --url: URL de la vidéo YouTube à télécharger.
- --title: Titre de la chanson.
- --artist: Nom de l'artiste.
- --output_folder: Dossier où les fichiers MP3 seront enregistrés. Par défaut, c'est ./output.
- --bitrate: Bitrate pour le fichier MP3. Par défaut, c'est 128k.