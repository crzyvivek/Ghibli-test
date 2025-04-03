from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

# प्लान्स की जानकारी
PLANS = {
    "Plan 1": {"price": 100, "photos": 10},
    "Plan 2": {"price": 250, "photos": 30},
    "Plan 3": {"price": 500, "photos": 50},
    "Plan 4": {"price": 1000, "photos": 250}
}

UPI_ID = "crzyvivek@ybl"
QR_CODE_LINK = "https://files.catbox.moe/dd0deu.jpg"

def show_plans(update, context: CallbackContext):
    """यूजर को प्लान्स दिखाने के लिए"""
    keyboard = [[InlineKeyboardButton(plan, callback_data=f"buy_{plan}")] for plan in PLANS.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("\U0001F4B8 उपलब्ध प्लान्स:\n", reply_markup=reply_markup)

def buy_plan(update, context: CallbackContext):
    """यूजर द्वारा प्लान खरीदने का ऑप्शन हैंडल करना"""
    query = update.callback_query
    plan_name = query.data.split("buy_")[1]
    plan_details = PLANS.get(plan_name, {})
    
    if plan_details:
        message = (f"\U0001F4B0 *{plan_name}* \n"
                   f"\U0001F4B5 Price: ₹{plan_details['price']}\n"
                   f"\U0001F4F7 Photos Limit: {plan_details['photos']}\n"
                   f"\U0001F4E6 Payment Method:\n"
                   f"- Send ₹{plan_details['price']} to *{UPI_ID}*\n"
                   f"- Scan QR Code below\n"
                   f"\U0001F4F8 [QR Code]({QR_CODE_LINK})")
        query.message.reply_text(message, parse_mode="Markdown")
    else:
        query.message.reply_text("❌ Invalid Plan Selected!")

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("plans", show_plans))
    dispatcher.add_handler(CallbackQueryHandler(buy_plan, pattern=r"buy_.*"))
