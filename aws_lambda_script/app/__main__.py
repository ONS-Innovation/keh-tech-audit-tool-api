from app import create_app

app = create_app()

# Needs to be run on port 8000 for the Cognito redirect URI.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
