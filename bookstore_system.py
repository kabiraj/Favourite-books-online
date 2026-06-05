from app import create_app
from flask_livereload import LiveReload

app = create_app()
LiveReload(app)

# macOS often uses port 5000 for AirPlay (returns 403 in the browser).
PORT = 5001

if __name__ == "__main__":
    print(f"\n  Open in your browser: http://127.0.0.1:{PORT}/browse\n")
    app.run(debug=True, host="127.0.0.1", port=PORT)
    