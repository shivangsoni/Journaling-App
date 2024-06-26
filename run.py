from app import create_app
import webbrowser
import threading

app = create_app()

def open_browser():
    webbrowser.open_new("http://localhost:5000")

if __name__ == '__main__':
    # Start a thread to open the browser after a short delay
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
