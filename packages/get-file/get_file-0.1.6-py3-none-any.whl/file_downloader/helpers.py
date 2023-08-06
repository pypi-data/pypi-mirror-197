import re

def check_filename(filename):
    """
    This function checks if a given filename is valid or not based on some basic criteria.
    It returns True if the filename is valid and False otherwise.
    """
    # Check if the filename is not empty
    if not filename:
        return False
    
    # Check if the filename contains only alphanumeric characters, underscores, dots, and hyphens
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        return False
    
    # Check if the filename has a valid extension (optional)
    valid_extensions = ['txt',
    'doc',
    'docx',
    'pdf',
    'xlsx',
    'pptx',
    'jpg',
    'png',
    'gif',
    'mp3',
    'mp4',
    'avi',
    'mov',
    'zip',
    'rar',
    'tar',
    'gz',
    'exe',
    'mkv']
    extension = filename.split('.')[-1]
    if extension not in valid_extensions:
        return False
    
    # If all checks pass, the filename is considered valid
    return True
