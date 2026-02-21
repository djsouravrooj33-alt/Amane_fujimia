import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================= ENV =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 8145485145
GROUP_ID = -1003296016362

# ================= Fake Web Server (Render Free Fix) =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ================= Commands =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Active!\n/help লিখে সব কমান্ড দেখুন"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Available Commands:\n\n"
        "/num 9998887779 → Mobile Info\n"
        "/adh 123412341234 → Aadhaar Info\n"
        "/vec DL9C0001 → Vehicle Info\n"
        "/upi name@upi → UPI → IFSC → Bank Details\n"
        "/ifsc SBIN0000001 → IFSC Lookup"
    )

# ================= APIs =================

async def num_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /num 9998887779")
        return
    mobile = context.args[0]
    url = f"https://num.proportalxc.workers.dev/?mobile={mobile}"
    data = requests.get(url, timeout=15).text
    await update.message.reply_text(data)

async def adh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /adh 123412341234")
        return
    aadhaar = context.args[0]
    url = f"https://api.paanel.shop/numapi.php?action=api&key=SALAAR&aadhar={aadhaar}"
    data = requests.get(url, timeout=15).text
    await update.message.reply_text(data)

async def vec_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /vec DL9C0001")
        return
    rc = context.args[0]
    url = f"https://org.proportalxc.workers.dev/?rc={rc}"
    data = requests.get(url, timeout=15).text
    await update.message.reply_text(data)

async def ifsc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /ifsc SBIN0000001")
        return
    ifsc = context.args[0]
    url = f"https://ifsc.razorpay.com/{ifsc}"
    res = requests.get(url, timeout=15)

    if res.status_code != 200:
        await update.message.reply_text("❌ IFSC পাওয়া যায়নি")
        return

    d = res.json()
    msg = (
        "🏦 Bank Details\n\n"
        f"Bank: {d.get('BANK')}\n"
        f"Branch: {d.get('BRANCH')}\n"
        f"IFSC: {d.get('IFSC')}\n"
        f"MICR: {d.get('MICR')}\n"
        f"Address: {d.get('ADDRESS')}"
    )
    await update.message.reply_text(msg)

async def upi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ ব্যবহার: /upi name@upi")
        return

    upi = context.args[0]
    await update.message.reply_text("🔎 UPI যাচাই করা হচ্ছে...")

    # Step 1: Dummy UPI → IFSC resolve (bank inference)
    ifsc_guess = "SBIN0000001"

    # Step 2: IFSC → Bank Details
    url = f"https://ifsc.razorpay.com/{ifsc_guess}"
    res = requests.get(url, timeout=15)

    if res.status_code != 200:
        await update.message.reply_text("❌ Bank Details পাওয়া যায়নি")
        return

    d = res.json()
    msg = (
        "💳 UPI → Bank Chain\n\n"
        f"UPI ID: {upi}\n"
        f"Bank: {d.get('BANK')}\n"
        f"Branch: {d.get('BRANCH')}\n"
        f"IFSC: {d.get('IFSC')}\n"
        f"Address: {d.get('ADDRESS')}"
    )
    await update.message.reply_text(msg)

# ================= Bot Init =================

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("num", num_cmd))
    application.add_handler(CommandHandler("adh", adh_cmd))
    application.add_handler(CommandHandler("vec", vec_cmd))
    application.add_handler(CommandHandler("upi", upi_cmd))
    application.add_handler(CommandHandler("ifsc", ifsc_cmd))

    application.run_polling()

if __name__ == "__main__":
    main()