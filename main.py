import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "9131381140:AAHpGjj5IVOBjA8MsGc_ZL3vpwd4eQ7EhUo"
BOT_USERNAME = "@Alomari_monitor_bot"

monitored_accounts = {}
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExM252N2FvY2Y5YXZ4ZmxubDNsMnQybm53bXp3YnF3OXJ1YnJvY3VidyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9J1nDfYtWbH3zSndbE/giphy.gif"
    
    await update.message.reply_animation(
        animation=gif_url,
        caption="👋 Welcome, my dear friend!\n\n🤖 I am your smart monitoring bot, working 24/7 to serve you.\n✨ Choose one of the options below to get started:"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Add account to monitoring", callback_data="add_account")],
        [InlineKeyboardButton("🗑️ Remove account", callback_data="remove_account")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("📌 Please choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "add_account":
        user_states[query.from_user.id] = {"step": "waiting_for_username"}
        await query.message.reply_text("✍️ Please send the account **Username** (e.g., @username):")
    elif query.data == "remove_account":
        await query.message.reply_text("🗑️ Please send the username you want to remove:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    photo = update.message.photo
    
    state = user_states.get(user_id, {})
    current_step = state.get("step")
    
    if current_step == "waiting_for_username":
        username = text if text.startswith("@") else f"@{text}"
        user_states[user_id]["username"] = username
        user_states[user_id]["step"] = "waiting_for_screenshot"
        
        await update.message.reply_text(
            f"🎯 Great! Username saved: **{username}**\n\n📸 Now, please send the **Ban Screenshot**:"
        )
        
    elif photo and current_step == "waiting_for_screenshot":
        user_states[user_id]["step"] = "waiting_for_ban_type"
        
        keyboard = [
            [InlineKeyboardButton("⚖️ Community Integrity", callback_data="ban_integrity")],
            [InlineKeyboardButton("🚨 Fraud & Scam", callback_data="ban_fraud")],
            [InlineKeyboardButton("🎭 Impersonation", callback_data="ban_impersonation")],
            [InlineKeyboardButton("🔞 NSFW & Nudity", callback_data="ban_nsfw")],
            [InlineKeyboardButton("📜 Copyright Violation", callback_data="ban_copyright")],
            [InlineKeyboardButton("⚠️ Spam & Harassment", callback_data="ban_spam")],
            [InlineKeyboardButton("🔒 Temporary Ban", callback_data="ban_temporary")],
            [InlineKeyboardButton("❌ Permanent Ban", callback_data="ban_permanent")],
            [InlineKeyboardButton("❓ Logout Fake / Other", callback_data="ban_other")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📥 Screenshot received successfully!\n🔍 Please select the **Ban Type** from the buttons below:",
            reply_markup=reply_markup
        )

async def ban_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    ban_types = {
        "ban_integrity": "Community Integrity Violation",
        "ban_fraud": "Fraud & Scam",
        "ban_impersonation": "Impersonation",
        "ban_nsfw": "NSFW & Nudity",
        "ban_copyright": "Copyright Violation",
        "ban_spam": "Spam & Harassment",
        "ban_temporary": "Temporary Ban",
        "ban_permanent": "Permanent Ban",
        "ban_other": "Logout Fake"
    }
    
    selected_ban = ban_types.get(query.data, "Logout Fake")
    state = user_states.get(user_id, {})
    username = state.get("username", "@unknown")
    
    start_dt = datetime.now()
    start_time_str = start_dt.strftime("%m/%d/%Y %I:%M:%S %p")
    
    monitored_accounts[user_id] = {
        "username": username,
        "ban_type": selected_ban,
        "start_dt": start_dt,
        "start_str": start_time_str
    }
    
    confirmation_message = (
        f"✅ **Account added to live monitoring successfully!**\n\n"
        f"👤 • **Username:** {username}\n"
        f"🏷️ • **Ban Type:** {selected_ban}\n"
        f"⏱️ • **Monitoring Started:** {start_time_str}\n"
        f"🤖 • **Monitored By:** {BOT_USERNAME}\n\n"
        f"💡 Send /start anytime to monitor another account."
    )
    
    await query.message.reply_text(confirmation_message, parse_mode="Markdown")
    
    if user_id in user_states:
        del user_states[user_id]

async def simulate_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in monitored_accounts:
        await update.message.reply_text("⚠️ No active monitored account found to simulate unban. Add an account first using /start")
        return
        
    acc = monitored_accounts[user_id]
    username = acc["username"]
    ban_type = acc["ban_type"]
    start_dt = acc["start_dt"]
    
    now_dt = datetime.now()
    diff = now_dt - start_dt
    
    hours, remainder = divmod(int(diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    tat_str = f"{hours}h {minutes}m {seconds}s"
    time_str = now_dt.strftime("%m/%d/%Y %I:%M:%S %p")
    
    unban_message = (
        f"🎉 You can use **{username}** again!\n\n"
        f"👤 • **Username:** {username}\n"
        f"⏳ • **TAT:** {tat_str}\n"
        f"🏷️ • **Type:** {ban_type}\n"
        f"⏰ • **Time:** {time_str}\n"
        f"🤖 • **By:** {BOT_USERNAME}"
    )
    
    await update.message.reply_text(unban_message, parse_mode="Markdown")
    del monitored_accounts[user_id]

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("unban_test", simulate_unban))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(add_account|remove_account)$"))
    app.add_handler(CallbackQueryHandler(ban_type_handler, pattern="^ban_"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    
    print("Bot is running with emojis...")
    app.run_polling()

if __name__ == "__main__":
    main()
