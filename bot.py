from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from utils import is_valid_url, check_rate_limit, ensure_storage
from tasks import perform_scan_task
import os

active_tasks = {}

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /scan <url> [--deep] [--type=ssl,headers]\nOnly scan sites you own."
    )

async def scan_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        return await update.message.reply_text("❌ Usage: /scan https://example.com [--deep] [--type=ssl,headers]")

    url = ctx.args[0]
    if not is_valid_url(url):
        return await update.message.reply_text("❌ Invalid URL")

    user = update.effective_user.id
    if not check_rate_limit(user):
        return await update.message.reply_text("❌ Rate limit reached (3/day)")

    deep = '--deep' in ctx.args
    scan_type = next((arg.split('=')[1] for arg in ctx.args if arg.startswith('--type=')), None)

    await update.message.reply_text(f"✅ Scan started for {url}")
    task = perform_scan_task.delay(url, deep, scan_type)
    active_tasks[task.id] = url
    await update.message.reply_text(f"⏳ Check status: /status {task.id}")

async def status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        return await update.message.reply_text("Usage: /status <task_id>")

    task_id = ctx.args[0]
    from tasks import perform_scan_task
    task = perform_scan_task.AsyncResult(task_id)
    if task.ready():
        scan_id, path = task.result
        with open(path) as f:
            content = f.read()
        await update.message.reply_text(f"✅ Scan results for {active_tasks.get(task_id, '')}:\n\n{content[:4000]}")
    else:
        await update.message.reply_text("⏳ Still scanning...")

def main():
    ensure_storage()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()

if __name__ == "__main__":
    main()
      
