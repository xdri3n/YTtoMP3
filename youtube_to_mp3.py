import os
import yt_dlp
from pydub import AudioSegment
import requests
import csv


def download_and_convert(url, title=None, artist=None, output_folder=".", bitrate="192k"):
    if title and artist:
        output_template = os.path.join(output_folder, f'{artist} - {title}.%(ext)s')
    else:
        output_template = os.path.join(output_folder, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate.replace("k", ""),
        }],
        'outtmpl': output_template,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")

    if title or artist:
        audio = AudioSegment.from_mp3(filepath)
        audio.export(filepath, format="mp3", tags={"artist": artist, "title": title})

    # Téléchargez la miniature
    thumbnail_url = info_dict['thumbnail']
    response = requests.get(thumbnail_url, stream=True)
    response.raise_for_status()
    with open("temp_thumbnail.webp", 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print("Thumbnail downloaded.")

    # Convertissez l'image WebP en JPEG et recadrez-la pour qu'elle soit carrée
    os.system(f'ffmpeg -i temp_thumbnail.webp -vf "crop=min(iw\,ih):min(iw\,ih)" temp_thumbnail.jpg')

    # Ajoutez la miniature au fichier MP3 comme image d'album
    output_with_image = filepath.replace(".mp3", "_with_image.mp3")
    os.system(f'ffmpeg -i "{filepath}" -i temp_thumbnail.jpg -c copy -map 0 -map 1 -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" "{output_with_image}"')
    os.remove(filepath)
    os.rename(output_with_image, filepath)
    print("Thumbnail added to mp3.")

    # Supprimez la miniature temporaire
    os.remove("temp_thumbnail.webp")
    os.remove("temp_thumbnail.jpg")
    print("Temporary thumbnails removed.")

# python3 youtube_to_mp3.py --csv "./video.csv" --output_folder "./output" --bitrate "128k"
def download_from_csv(csv_path, output_folder="./output", bitrate="192k"):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row['url']
            artist = row['artist']
            title = row['title']
            download_and_convert(url, title=title, artist=artist, output_folder=output_folder, bitrate=bitrate)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download YouTube videos and convert them to MP3.")
    parser.add_argument("--csv", help="Path to the CSV file containing the video URLs, artists, and titles.", default="./video.csv")
    parser.add_argument("--url", help="URL of the YouTube video.", default=None)
    parser.add_argument("--title", help="Title for the output MP3 file.", default=None)
    parser.add_argument("--artist", help="Artist for the output MP3 file.", default=None)
    parser.add_argument("--output_folder", help="Folder to save the output MP3 files.", default="./output")
    parser.add_argument("--bitrate", help="Bitrate for the output MP3 files.", default="128k")

    args = parser.parse_args()

    if args.csv:
        download_from_csv(args.csv, output_folder=args.output_folder, bitrate=args.bitrate)
    elif args.url:
        download_and_convert(args.url, title=args.title, artist=args.artist, output_folder=args.output_folder, bitrate=args.bitrate)
    else:
        print("Please provide either a CSV file or a YouTube URL.")
