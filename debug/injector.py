import sys
import os

LOG_FILE = "VCSdebug.log"

def custom_write(text):   
    with open(LOG_FILE, "a") as f:
        f.write(text)

sys.stdout.write = custom_write
sys.stderr.write = custom_write