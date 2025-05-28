from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

def validate_signup_data(data):
    errors = []

    if not data["username"] or not data["password"] or not data["user_type"]:
        errors.append("All fields are required.")

    if data["user_type"] not in ["user", "admin", "superadmin"]:
        errors.append("Invalid user type selected.")

    if User.objects.filter(username=data["username"]).exists():
        errors.append("Username already exists.")

    if len(data["password"]) < 6:
        errors.append("Password must be at least 6 characters long.")

    return errors


def validate_login_data(data):
    errors = []
    if not data['username']:
        errors.append("Username is required.")
    if not data['password']:
        errors.append("Password is required.")
    return errors


def validate_task_data(data):
    errors = []

    if not data.get('title'):
        errors.append("Title is required.")
    if not data.get('description'):
        errors.append("Description is required.")
    # if not data.get('admin'):
    #     errors.append("Admin is required.")
    if not data.get('assigned_to'):
        errors.append("Assigned user is required.")
    if not data.get('due_date'):
        errors.append("Due date is required.")
    else:
        try:
            due_date = date.fromisoformat(data['due_date'])
            if due_date < date.today():
                errors.append("Due date cannot be in the past.")
        except ValueError:
            errors.append("Invalid due date format. Use YYYY-MM-DD.")

    return errors


def validate_completion_report_data(data):
    errors = []
    report = data.get('completion_report', '').strip()
    if not report:
        errors.append("Completion report is required.")
    return errors
