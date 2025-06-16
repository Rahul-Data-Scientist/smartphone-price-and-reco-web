import os
import gdown


def download_file_from_google_drive(file_id, destination):
    if not os.path.exists(destination):
        print(f"Downloading {destination}...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, destination, quiet=False)
    else:
        print(f"{destination} already exists.")
