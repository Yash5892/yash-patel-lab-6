import requests
import hashlib
import os
import subprocess

def get_expected_sha256():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/SHA256SUMS"
    response = requests.get(url)
    response.raise_for_status()
    for line in response.text.splitlines():
        if "vlc-3.0.17.4-win64.exe" in line:
            return line.split()[0]
    raise ValueError("Expected SHA-256 hash not found in the file.")

def download_installer():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe"
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def installer_ok(installer_data, expected_sha256):
    sha256 = hashlib.sha256(installer_data).hexdigest()
    return sha256 == expected_sha256

def save_installer(installer_data):
    temp_dir = os.getenv('TEMP')
    installer_path = os.path.join(temp_dir, "vlc-3.0.17.4-win64.exe")
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    return installer_path

def run_installer(installer_path):
    subprocess.run([installer_path, '/S'], check=True)

def delete_installer(installer_path):
    os.remove(installer_path)

def main():
    try:
        # Get the expected SHA-256 hash value of the VLC installer
        expected_sha256 = get_expected_sha256()
        print("Expected SHA-256 hash:", expected_sha256)

        # Download (but don't save) the VLC installer from the VLC website
        installer_data = download_installer()
        print("Installer downloaded.")

        # Verify the integrity of the downloaded VLC installer by comparing the expected and computed SHA-256 hash values
        if installer_ok(installer_data, expected_sha256):
            print("Installer integrity verified.")

            # Save the downloaded VLC installer to disk
            installer_path = save_installer(installer_data)
            print("Installer saved to:", installer_path)

            # Silently run the VLC installer
            run_installer(installer_path)
            print("Installer executed.")

            # Delete the VLC installer from disk
            delete_installer(installer_path)
            print("Installer deleted.")
        else:
            print("Installer integrity verification failed.")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()