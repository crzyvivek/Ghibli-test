import os
import json
import logging
from database import Database
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()

def load_config():
    """Load bot configuration from a JSON file."""
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

config = load_config()

def get_payment_qr():
    """Return payment QR code URL and UPI ID."""
    return config.get("payment_qr", ""), config.get("upi_id", "")

def get_admin():
    """Return admin username."""
    return config.get("admin_username", "@admin")

def create_main_menu():
    """Create main menu buttons."""
    keyboard = [[
        InlineKeyboardButton("Create Edit", callback_data="create_edit"),
        InlineKeyboardButton("Buy Plan", callback_data="buy_plan")
    ], [
        InlineKeyboardButton("My Plan", callback_data="my_plan"),
        InlineKeyboardButton("About", callback_data="about")
    ], [
        InlineKeyboardButton("Contact Support", callback_data="contact_support"),
        InlineKeyboardButton("Free Edit", callback_data="free_edit")
    ]]
    return InlineKeyboardMarkup(keyboard)

def get_user_plan(user_id):
    """Fetch the user's current plan from the database."""
    return db.get_plan(user_id)

def update_user_plan(user_id, plan):
    """Update user plan in the database."""
    db.update_plan(user_id, plan)

def check_plan_limit(user_id):
    """Check if the user has reached their plan limit."""
    plan = get_user_plan(user_id)
    if plan and plan["remaining"] > 0:
        return True
    return False

def decrement_plan_limit(user_id):
    """Reduce the user's remaining edit count."""
    plan = get_user_plan(user_id)
    if plan and plan["remaining"] > 0:
        plan["remaining"] -= 1
        update_user_plan(user_id, plan)
        return True
    return False
