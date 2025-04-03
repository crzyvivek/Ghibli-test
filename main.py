# main.py - Telegram Bot Main File

import logging
import telebot
import database

# Bot Token & Admin Details
BOT_TOKEN = "7733834389:AAGAI9Iifgv5KHpvVn1S9crEp4xY-hFFbpQ"
ADMIN_USERNAME = "@crzy_vivek"
WHATSAPP_LINK = "https://wa.me/qr/OKTN7MRAWI3CH1"
QR_CODE_LINK = "https://files.catbox.moe/dd0deu.jpg"
UPI_ID = "crzyvivek@ybl"
TELEGRAM_ID = 1528171780  # Your Telegram ID

# Initialize Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Logging
logging.basicConfig(level=logging.INFO)

# Plans
PLANS = {
    "Plan 1": {"price": 100, "photos": 10},
    "Plan 2": {"price": 250, "photos": 30},
    "Plan 3": {"price": 500, "photos": 50},
    "Plan 4": {"price": 1000, "photos": 250},
}

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    username = message.chat.username
    database.add_user(user_id, username)
    
    welcome_text = f"👋 **Welcome {username}!**\n\n📸 *This is your AI Photo Editing Bot.*\n\n"
    welcome_text += "**Options:**\n"
    welcome_text += "1️⃣ Create/Edit Photos\n"
    welcome_text += "2️⃣ Buy Plans\n"
    welcome_text += "3️⃣ My Plan\n"
    welcome_text += "4️⃣ Contact Support\n"
    welcome_text += "5️⃣ About Us\n"
    
    bot.send_message(user_id, welcome_text)

# Show Available Plans
@bot.message_handler(commands=['buy'])
def show_plans(message):
    user_id = message.chat.id
    plan_text = "📜 **Available Plans:**\n\n"
    
    for plan, details in PLANS.items():
        plan_text += f"🔹 {plan} - ₹{details['price']} | {details['photos']} photos\n"
    
    plan_text += f"\n💳 **Payment Details:**\n🔹 UPI: `{UPI_ID}`\n🔹 QR Code: [Click Here]({QR_CODE_LINK})\n"
    plan_text += "📩 Send payment screenshot to admin for activation."

    bot.send_message(user_id, plan_text, parse_mode="Markdown")

# Check User Plan
@bot.message_handler(commands=['myplan'])
def my_plan(message):
    user_id = message.chat.id
    user = database.get_user(user_id)
    
    if user and user[3]:
        plan_text = f"📝 **Your Plan:** {user[3]}\n📸 Photos Used: {user[2]}"
    else:
        plan_text = "❌ You haven't purchased any plan yet. Use /buy to get one."

    bot.send_message(user_id, plan_text)

# Contact Support
@bot.message_handler(commands=['contact'])
def contact_support(message):
    user_id = message.chat.id
    contact_text = f"📞 **Support Details:**\n🔹 Admin: {ADMIN_USERNAME}\n🔹 WhatsApp: [Click Here]({WHATSAPP_LINK})\n🔹 Telegram: [Click Here](tg://user?id={TELEGRAM_ID})"
    bot.send_message(user_id, contact_text, parse_mode="Markdown")

# About Us
@bot.message_handler(commands=['about'])
def about(message):
    user_id = message.chat.id
    about_text = "🤖 **About This Bot:**\nThis bot allows you to create & edit high-quality AI photos. Powered by advanced AI algorithms."
    bot.send_message(user_id, about_text)

# Handle Photo Upload
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    user = database.get_user(user_id)

    if not user or not user[3]:
        bot.send_message(user_id, "❌ You need to buy a plan first. Use /buy")
        return

    plan = PLANS.get(user[3])
    
    if user[2] >= plan["photos"]:
        bot.send_message(user_id, "⚠️ Your plan limit is over! Buy a new plan to continue.")
        return
    
    database.update_photo_usage(user_id)
    bot.send_message(user_id, "✅ Photo received! Processing now...")

# Run Bot
bot.polling()
