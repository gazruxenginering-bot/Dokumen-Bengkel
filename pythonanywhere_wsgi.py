"""
PythonAnywhere WSGI Configuration for Google Drive File Browser
Place this file at: /var/www/gazruxenginering_pythonanywhere_com_wsgi.py
"""

import sys
import os

# Add project directory to path
project_dir = '/home/gazruxenginering/google-drive-browser'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set working directory
os.chdir(project_dir)

# Import Flask app
from app import app as application
