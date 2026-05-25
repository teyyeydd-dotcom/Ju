import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import json

BOT_TOKEN = "8916367639:AAEES5AfYW80gfPI36Q-mM6BqpbNet4oYJ8"
API_URL = "https://usersxinfo-admin.onrender.com/api"

CHANNEL_ID = -1003742200553
CHANNEL_LINK = "https://t.me/+xh6dCJU5DgxmMDJl"

# =========================
# CHECK JOIN
# =========================
async def is_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# =========================
# BUTTON UI
# =========================
def join_buttons():
    keyboard = [
        [InlineKeyboardButton("🔐 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")]
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# API
# =========================
def get_data(number):
    try:
        params = {
            "key": "nfttth",
            "type": "mobile",
            "term": number
        }

        res = requests.get(API_URL, params=params, timeout=10)
        data = res.json()

        data.pop("tag", None)
        data["developer"] = "@JEHRELA_PAPA"

        return data

    except:
        return {"error": "API Error"}

# =========================
# SPLIT MSG
# =========================
def split_msg(text, size=4000):
    return [text[i:i+size] for i in range(0, len(text), size)]

async def send_long(update, text):
    for part in split_msg(text):
        await update.message.reply_text(part)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_joined(user_id, context):
        await update.message.reply_text(
            "🚫 Access Denied!\n\n"
            "👉 Please join our private channel first.\n"
            "Then click ✅ Verify.",
            reply_markup=join_buttons()
        )
        return

    await update.message.reply_text(
        "Welcome to addar bot by @jehrelaxwify\n\n"
        "Regards heykavin\n\n"
        "For free users ❤️"
    )

# =========================
# VERIFY BUTTON
# =========================
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_joined(user_id, context):
        await query.answer("✅ Verified Successfully!")
        await query.message.reply_text(
            "🎉 You are verified!\n\nSend mobile number now."
        )
    else:
        await query.answer("❌ You have not joined yet!", show_alert=True)

# =========================
# HANDLE MESSAGE
# =========================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Force Join Check
    if not await is_joined(user_id, context):
        await update.message.reply_text(
            "🚫 Please join channel first!",
            reply_markup=join_buttons()
        )
        return

    # Number Check
    if text.isdigit() and len(text) == 10:
        msg = await update.message.reply_text("🔍 Searching...")

        data = get_data(text)
        result = json.dumps(data, indent=2)

        await send_long(update, result)

        await msg.delete()
    else:
        await update.message.reply_text("❌ Send valid 10-digit number")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("✅ Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()