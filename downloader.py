import gdown


def download_file_from_google_drive(file_id, destination):
    # Construct the direct URL
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False, fuzzy=True)
