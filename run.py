import os
from app import create_app
from database.database import db

# Create the app instance.
app = create_app()

if __name__ == "__main__":
    # Determine the port. Use the PORT environment variable if it's set,
    # otherwise default to 5000. This is good practice for deployment.
    port = int(os.environ.get("PORT", 5000))
    # Create the database and tables if they don't exist.
    with app.app_context():
        db.create_all()
    # Run the application.
    app.run(debug=True, host="0.0.0.0", port=port)
