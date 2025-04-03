from telegram import Update
from telegram.ext import CallbackContext
from database import get_user_plan, update_user_plan, check_photo_limit
from payment import process_payment
from photo_edit import process_edit_request

# Command Handlers
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_message = (f"Welcome {user.first_name}!\n"
                       "Use the menu below to navigate:")
    update.message.reply_text(welcome_message)


def my_plan(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    plan_details = get_user_plan(user_id)
    update.message.reply_text(plan_details)


def buy_plan(update: Update, context: CallbackContext):
    plans_info = "Available Plans:\n1. ₹100 - 10 Photos\n2. ₹250 - 30 Photos\n3. ₹500 - 50 Photos\n4. ₹1000 - 250 Photos"
    update.message.reply_text(plans_info)


def process_payment_request(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    amount = context.args[0] if context.args else None
    if not amount:
        update.message.reply_text("Please provide an amount to proceed.")
        return
    
    payment_link = process_payment(user_id, amount)
    update.message.reply_text(f"Complete your payment here: {payment_link}")


def create_edit(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if check_photo_limit(user_id):
        update.message.reply_text("Send the photo you want to edit.")
    else:
        update.message.reply_text("Your photo limit is over. Please buy a new plan.")


def handle_photo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    
    if not check_photo_limit(user_id):
        update.message.reply_text("Your plan limit is over. Buy a new plan.")
        return
    
    update.message.reply_text("Processing your photo... Please wait.")
    edited_photo = process_edit_request(photo)
    update.message.reply_photo(photo=edited_photo)
    update_user_plan(user_id)


def contact_support(update: Update, context: CallbackContext):
    support_message = "For support, contact us:\n"
    support_message += "WhatsApp: https://wa.me/qr/OKTN7MRAWI3CH1\n"
    support_message += "Telegram: @crzy_vivek"
    update.message.reply_text(support_message)
