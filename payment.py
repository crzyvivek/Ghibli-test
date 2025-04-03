import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Payment details
UPI_ID = "crzyvivek@ybl"
QR_CODE_LINK = "https://files.catbox.moe/dd0deu.jpg"

# Payment Plans
PAYMENT_PLANS = {
    "Plan 1": (100, "10 photos"),
    "Plan 2": (250, "30 photos"),
    "Plan 3": (500, "50 photos"),
    "Plan 4": (1000, "250 photos")
}

def show_payment_plans(update: Update, context: CallbackContext):
    """Send payment plans to the user."""
    keyboard = []
    for plan, (price, photos) in PAYMENT_PLANS.items():
        keyboard.append([InlineKeyboardButton(f"{plan} - ₹{price} ({photos})", callback_data=f"buy_{plan}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("\U0001F4B0 *Choose a payment plan:*", parse_mode="Markdown", reply_markup=reply_markup)

def handle_payment(update: Update, context: CallbackContext):
    """Handle payment button clicks."""
    query = update.callback_query
    query.answer()
    
    selected_plan = query.data.replace("buy_", "")
    price, photos = PAYMENT_PLANS[selected_plan]
    
    payment_message = (f"✅ *Payment Details:*
\n💳 *Plan:* {selected_plan}
📸 *Photos:* {photos}
💰 *Price:* ₹{price}
\n📌 *UPI ID:* `{UPI_ID}`
🖼️ *Scan QR to Pay:* [Click Here]({QR_CODE_LINK})")
    
    query.message.reply_text(payment_message, parse_mode="Markdown", disable_web_page_preview=False)
    query.message.reply_text("After payment, send the transaction screenshot to @crzy_vivek for activation.")

logging.info("Payment module loaded successfully!")
