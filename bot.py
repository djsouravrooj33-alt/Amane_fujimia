import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# ========== ENV ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 8145485145
GROUP_ID = -1003296016362

# ========== Flask Web Server (Render Free Fix) ==========
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# ========== ACCESS CONTROL ==========
def allowed(update: Update):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    return chat_id == GROUP_ID or user_id == OWNER_ID

# ========== COMMANDS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    await update.message.reply_text(
        "🤖 Bot Active\n/help লিখে সব কমান্ড দেখুন"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    await update.message.reply_text(
        "📌 Available Commands:\n\n"
        "/num 9998887779\n"
        "/adh 123412341234\n"
        "/vec DL9C0001\n"
        "/upi name@upi\n"
        "/ifsc SBIN0000001"
    )

# -------- Phone Number (JSON Parse) --------
async def num_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /num 9998887779")
        return

    mobile = context.args[0]
    url = f"https://num.proportalxc.workers.dev/?mobile={mobile}"

    try:
        r = requests.get(url, timeout=15).json()

        msg = (
            f"📱 Mobile: {mobile}\n"
            f"👤 Name: {r.get('name','N/A')}\n"
            f"📍 Circle: {r.get('circle','N/A')}\n"
            f"📡 Operator: {r.get('operator','N/A')}"
        )
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ Number API Error")

# -------- Aadhaar (JSON Parse) --------
async def adh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /adh 123412341234")
        return

    aadhaar = context.args[0]
    url = f"https://api.paanel.shop/numapi.php?action=api&key=SALAAR&aadhar={aadhaar}"

    try:
        r = requests.get(url, timeout=20).json()

        msg = (
            f"🆔 Aadhaar: {aadhaar}\n"
            f"👤 Name: {r.get('name','N/A')}\n"
            f"🎂 DOB: {r.get('dob','N/A')}\n"
            f"⚧ Gender: {r.get('gender','N/A')}\n"
            f"📍 Address: {r.get('address','N/A')}"
        )
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ Aadhaar API Error")

# -------- Vehicle (JSON Parse) --------
async def vec_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /vec DL9C0001")
        return

    rc = context.args[0].lower()
    url = f"https://org.proportalxc.workers.dev/?rc={rc}"

    try:
        r = requests.get(url, timeout=20).json()

        msg = (
            f"🚗 Vehicle No: {rc.upper()}\n"
            f"👤 Owner: {r.get('owner','N/A')}\n"
            f"🏷 Model: {r.get('model','N/A')}\n"
            f"🏢 RTO: {r.get('rto','N/A')}\n"
            f"⛽ Fuel: {r.get('fuel','N/A')}"
        )
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ Vehicle API Error")

# -------- IFSC Lookup --------
async def ifsc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /ifsc SBIN0000001")
        return

    ifsc = context.args[0]

    try:
        r = requests.get(f"https://ifsc.razorpay.com/{ifsc}", timeout=15)
        d = r.json()

        msg = (
            f"🏦 Bank: {d['BANK']}\n"
            f"🔢 IFSC: {d['IFSC']}\n"
            f"🏢 Branch: {d['BRANCH']}\n"
            f"📍 Address: {d['ADDRESS']}"
        )
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ IFSC API Error")

# -------- UPI → IFSC → Bank --------
async def upi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /upi name@upi")
        return

    upi = context.args[0]
    ifsc = "SBIN0000001"  # demo resolve

    try:
        r = requests.get(f"https://ifsc.razorpay.com/{ifsc}", timeout=15)
        d = r.json()

        msg = (
            f"💳 UPI ID: {upi}\n"
            f"🏦 Bank: {d['BANK']}\n"
            f"🔢 IFSC: {d['IFSC']}\n"
            f"🏢 Branch: {d['BRANCH']}"
        )
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ UPI Resolve Error")

# ========== MAIN ==========
def main():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help_cmd))
    bot.add_handler(CommandHandler("num", num_cmd))
    bot.add_handler(CommandHandler("adh", adh_cmd))
    bot.add_handler(CommandHandler("vec", vec_cmd))
    bot.add_handler(CommandHandler("ifsc", ifsc_cmd))
    bot.add_handler(CommandHandler("upi", upi_cmd))

    bot.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()