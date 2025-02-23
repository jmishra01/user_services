
import frappe

# from frappe import STANDARD_USERS, _, msgprint, throw
from frappe.core.doctype.user.user import User



@frappe.whitelist(methods=["POST"])
def create_user(email, first_name, last_name, role_profile_name: str | None = None, password: str | None = None):
    if frappe.db.exists("User", email):
        return {"status": "error", "message": "User already exists"}

    user: User = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "enabled": 1,
        "send_welcome_email": 0,
        "role_profile_name": role_profile_name
    })

    user.insert(ignore_permissions=True)
    frappe.db.commit()

    # Set the password
    user.new_password = password if password else "abcde12345"
    user.save()
    frappe.db.commit()

    return {"status": "success", "message": "User created and password set", "user": user.name}


@frappe.whitelist(methods=["POST"])
def deactivate_user(email):
    if not frappe.db.exists("User", email):
        return {"status": "error", "message": "User does not exist"}

    user = frappe.get_doc("User", email)
    user.enabled = 0
    user.save()
    frappe.db.commit()

    return {"status": "success", "message": f"User {email} has been deactivated"}


@frappe.whitelist(methods=["POST"])
def activate_user(email):
    if not frappe.db.exists("User", email):
        return {"status": "error", "message": "User does not exist"}

    user = frappe.get_doc("User", email)
    user.enabled = 1
    user.save()
    frappe.db.commit()

    return {"status": "success", "message": f"User {email} has been activated"}
