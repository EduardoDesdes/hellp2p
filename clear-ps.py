import os

os.system("netstat -putona | grep python | awk '{print $7}' | cut -d '/' -f 1 | xargs kill -9")