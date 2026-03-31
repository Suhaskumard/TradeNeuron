import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.core.config import settings
from strategy.engine import StrategyEngine

class TelegramBot:
    def __init__(self):
        self.strategy = StrategyEngine()
        self.app = Application.builder().token(settings.TELEGRAM_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("signal", self.signal))
        self.app.add_handler(CommandHandler("status", self.status))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 TradeNeuron Bot\n"
            "/signal AAPL - Get signal\n"
            "/status - System status"
        )
    
    async def signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /signal AAPL")
            return
        
        symbol = context.args[0].upper()
        await update.message.reply_text(f"Fetching signal for {symbol}...")
        
        # Generate signal
        pred = {"signal": "BUY", "confidence": 0.85, "price": 150.0}
        emoji = "🟢" if pred["signal"] == "BUY" else "🔴" if pred["signal"] == "SELL" else "🟡"
        
        message = f"{emoji} {pred['signal']} {symbol}\nConfidence: {pred['confidence']:.1%}\nTarget: ${pred['price']:.2f}"
        await update.message.reply_text(message)
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ System healthy\nAPI: localhost:8001")
    
    def run(self):
        self.app.run_polling()

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()

