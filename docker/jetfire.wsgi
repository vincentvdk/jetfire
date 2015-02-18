#{{ ansible_managed}}

import sys
sys.stdout = sys.stderr
sys.path.insert(0, '/var/www/html/jetfire')
from app import app as application
