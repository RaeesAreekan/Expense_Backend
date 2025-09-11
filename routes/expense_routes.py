from flask import Blueprint, request, jsonify
from controllers.expense_controller import (
    add_expense_logic,
    get_expenses_logic,
    delete_expenses_logic,
)

# Create a Blueprint, which is a way to organize a group of related routes.
expense_blueprint = Blueprint("expenses", __name__)


@expense_blueprint.route("/", methods=["GET"])
def health_check():
    """
    A simple health check endpoint to confirm the API is running.
    This will be accessible at the root of the blueprint (e.g., /api/).
    """
    return jsonify({"status": "ok", "message": "Expense App API is running."}), 200


# Added two apis
@expense_blueprint.route("/expenses", methods=["POST"])
def add_expense_route():
    """
    API endpoint to add a new expense record.
    It passes the request data to the controller for processing.
    """
    data = request.get_json()
    return add_expense_logic(data)


@expense_blueprint.route("/expenses", methods=["GET"])
def get_expenses_route():
    """
    API endpoint to fetch all expenses, with optional date filters.
    """
    filters = request.args.to_dict()
    return get_expenses_logic(filters)


@expense_blueprint.route("/expenses", methods=["DELETE"])
def delete_expenses_route():
    """
    API endpoint to delete expenses based on a list of IDs.
    """
    data = request.get_json()
    ids = data.get("ids", [])
    return delete_expenses_logic(ids)
