from ..database.database import db
from ..models.expense import Expense
from flask import jsonify
from datetime import datetime
from sqlalchemy import extract
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="expense_tracker_app")


# --- New Function for Geocoding with Filtering ---
def get_location_name(latitude, longitude):
    """
    Converts latitude and longitude to a human-readable address using geopy,
    and returns the first 5 comma-separated components.
    """
    if not latitude or not longitude:
        return "Location Not Available"

    try:
        location = geolocator.reverse(f"{latitude},{longitude}", timeout=5)
        if location:
            # Split the full address by comma and take the first 5 parts
            req_fields = [
                "neighbourhood",
                "suburb",
                "city_district",
                "county",
                "postcode",
            ]
            add_comp = location.raw.get("address", {})
            filtered_address = ", ".join(
                add_comp.get(field) for field in req_fields if add_comp.get(field)
            )
            return filtered_address
        else:
            return "Unknown Location"
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return "Geocoding Service Unavailable"
    except Exception as e:
        print(f"An unexpected error occurred during geocoding: {e}")
        return "Unknown Location"


def add_expense_logic(data):
    """
    Handles the core logic for adding an expense.
    This function is now separate from the route definition.
    """
    try:
        price = data.get("price")
        name = data.get("name")
        shop_name = data.get("shopName")
        location = data.get("location", {})

        if not all([price, name]):
            return jsonify({"error": "Missing required fields: price and name."}), 400

        new_expense = Expense(
            price=price,
            name=name,
            shop_name=shop_name,
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
        )

        db.session.add(new_expense)
        db.session.commit()

        return (
            jsonify({"message": "Expense added successfully!", "id": new_expense.id}),
            201,
        )

    except Exception as e:
        print(f"Error adding expense: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


def get_expenses_logic(filters):
    """
    Fetches expenses from the database with optional date filters.
    """
    try:
        query = db.session.query(Expense)

        # Apply filters if they exist
        if filters.get("day"):
            query = query.filter(
                extract("day", Expense.timestamp) == int(filters["day"])
            )
        if filters.get("month"):
            query = query.filter(
                extract("month", Expense.timestamp) == int(filters["month"])
            )
        if filters.get("year"):
            query = query.filter(
                extract("year", Expense.timestamp) == int(filters["year"])
            )

        expenses = query.all()

        # Convert the expense objects to a list of dictionaries for JSON serialization
        expense_list = []
        for expense in expenses:
            location_name = get_location_name(expense.latitude, expense.longitude)
            expense_list.append(
                {
                    "id": expense.id,
                    "price": expense.price,
                    "name": expense.name,
                    "shopName": expense.shop_name,
                    "location": location_name,
                    "timestamp": expense.timestamp.isoformat(),
                }
            )

        return jsonify(expense_list), 200

    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
