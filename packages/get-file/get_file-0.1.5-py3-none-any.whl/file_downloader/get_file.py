from threading import Thread
import os
from helpers import check_filename
from datetime import datetime

"""
Author
    Ahtesham Zaidi
    
"""


def download_files(links: list) -> None:
    """
    Downloads all the links in the list asynchronously using separate threads.

    Args:
        links (list): A list of links to download.

    Returns:
        None
    """
    for link in links:
        """Iterates through all links in the links list and downloads them asynchronously."""
        Thread(target=download, args=(link,)).start()


def download(link: str) -> None:
    """
    Downloads a single file from the given link.

    Args:
        link (str): The link to the file to download.

    Returns:
        None
    """
    try:

        filename = link.split("/")[-1]
        cmd = rf'curl {link} --output {filename}'

        if check_filename(filename):
            print(f'Downloading file :: {link} ..... \n')
            os.system(cmd)
            print(f'Downloading finished :: {link} ..... \n')
        else:
            print(f'\nLink should contain filename\nFor example : \n\t www.example.com/file.pdf \n')
        
    except:
        print("Something is wrong with the download link")


if __name__ == "__main__":
    download('www.example.com')
    download_files(['https://example.com/file1.mp3',
                   'https://example.com/file2.mp3', 'https://example.com/file.pdf'])
