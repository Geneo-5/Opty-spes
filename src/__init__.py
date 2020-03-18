from srv.server import start
# import webbrowser
import webview

if __name__ == "__main__":
    #webbrowser.open('http://localhost:31415')
    start()
    webview.create_window('Hello world', 'http://localhost:31415')
    webview.start(http_server=True, debug=True)