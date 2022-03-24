"""Application entry point."""
from app import init_app

app = init_app()

if __name__ == "__main__":
    app.run(debug=False, port=8050)
