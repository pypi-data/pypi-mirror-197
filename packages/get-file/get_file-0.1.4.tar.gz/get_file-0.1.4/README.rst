.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/file_downloader.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/file_downloader
    .. image:: https://readthedocs.org/projects/file_downloader/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://file_downloader.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/file_downloader/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/file_downloader
    .. image:: https://img.shields.io/pypi/v/file_downloader.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/file_downloader/
    .. image:: https://img.shields.io/conda/vn/conda-forge/file_downloader.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/file_downloader
    .. image:: https://pepy.tech/badge/file_downloader/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/file_downloader
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/file_downloader

.. .. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
..     :alt: Project generated with PyScaffold
..     :target: https://pyscaffold.org/

.. |

=========
get-file
=========


    Download any file asynchronously with ease using this Python package available on PyPi.


This Python package is designed to simplify the process of downloading files asynchronously. 
With its easy-to-use interface, users can quickly and efficiently download any file from the internet without the need for complex coding. 
Whether you're downloading large ones, small ones, single or multiple files this package is built to handle it all.

This package utilizes concept of Multi-Threading to perform downloads asynchronously, which means that the download process won't block the main thread and can continue to run in the background while other tasks are being performed. 
This feature makes it ideal for developers who need to download large volumes of files or who want to create applications that require efficient file downloading.

In addition, this package is available on PyPi, which means that it can be easily installed using pip. 
Once installed, you can import it into your Python code and start using it right away. 
With its simple and straightforward API, downloading files asynchronously has never been easier.


Installation
------------


    ``pip install get-file``

Usage
-----

    Download Single File :

     ``from file_downloader import get_file``
     
     ``get_file.download("https://example.com/file.mp3")``

    Download Multiple Files :

        ``from file_downloader import get_file``
        
        ``get_file.download_files(["https://example.com/file1.mp3", "https://example.com/file2.pdf"])``

