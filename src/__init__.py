import sys
import webbrowser
from srv.server import start

if __name__ == "__main__":
    webbrowser.open('http://localhost:31415')
    start()
    sys.exit()