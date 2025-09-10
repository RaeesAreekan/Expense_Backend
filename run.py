from app import create_app
from database.database import db

# Create the app instance.
app = create_app()

if __name__ == "__main__":
    # Create the database and tables if they don't exist.
    with app.app_context():
        db.create_all()
    # Run the application.
    app.run(debug=True, port=5000)
