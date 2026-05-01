import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token (Environment Variable ကနေ ယူပါ)
TOKEN = os.environ.get("BOT_TOKEN")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Flask app for health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@app.route('/health')
def health_check():
    return "OK", 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 မင်္ဂလာပါ။ PTK Streaming Bot မှ ကြိုဆိုပါတယ်။\n\n/movies နှိပ်ပြီး ရုပ်ရှင်စာရင်းကြည့်ပါ။")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📖 အကူအညီ\n\n/movies - ရုပ်ရှင်စာရင်း\n/search [နာမည်] - ရှာဖွေရန်\n/genre - အမျိုးအစားအလိုက်\n/request - ရုပ်ရှင်တောင်းဆိုရန်\n/latest - အသစ်ထည့်သွင်းထားသော\n/popular - လူကြိုက်များသော\n/download - ဒေါင်းလုဒ်လင့်\n/stream - တိုက်ရိုက်ကြည့်ရန်")

# /movies command
async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Action", callback_data="action"),
         InlineKeyboardButton("😱 Horror", callback_data="horror")],
        [InlineKeyboardButton("😂 Comedy", callback_data="comedy"),
         InlineKeyboardButton("💕 Romance", callback_data="romance")],
        [InlineKeyboardButton("🎥 Drama", callback_data="drama"),
         InlineKeyboardButton("🤖 Sci-Fi", callback_data="scifi")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📽️ ရုပ်ရှင်အမျိုးအစား ရွေးပါ။", reply_markup=reply_markup)

# /search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        query = " ".join(context.args)
        await update.message.reply_text(f"🔍 '{query}' ကိုရှာဖွေနေပါသည်...\n\n(ဒေတာဘေ့စ်မရှိသေးပါ။ နောက်ပိုင်းထည့်ပေးပါမည်။)")
    else:
        await update.message.reply_text("🔍 ရုပ်ရှင်နာမည်ထည့်ပေးပါ။\nဥပမာ - /search Spider Man")

# /genre command
async def genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Action", callback_data="action"),
         InlineKeyboardButton("😱 Horror", callback_data="horror")],
        [InlineKeyboardButton("😂 Comedy", callback_data="comedy"),
         InlineKeyboardButton("💕 Romance", callback_data="romance")],
        [InlineKeyboardButton("🎥 Drama", callback_data="drama"),
         InlineKeyboardButton("🤖 Sci-Fi", callback_data="scifi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎭 အမျိုးအစားတစ်ခုခုကို ရွေးပါ။", reply_markup=reply_markup)

# /request command
async def request_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        movie_name = " ".join(context.args)
        await update.message.reply_text(f"✅ '{movie_name}' ရုပ်ရှင်တောင်းဆိုမှုကို လက်ခံပါပြီ။\nမကြာမီထည့်သွင်းပေးပါမည်။")
    else:
        await update.message.reply_text("📝 ရုပ်ရှင်နာမည်ထည့်ပေးပါ။\nဥပမာ - /request Avatar 2")

# /latest command
async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆕 ဒီနေ့ထည့်သွင်းထားသော ရုပ်ရှင်အသစ်များ:\n\n1. Deadpool 3\n2. Inside Out 2\n3. Furiosa\n4. Kingdom of the Planet of the Apes")

# /popular command
async def popular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 လူကြိုက်အများဆုံးရုပ်ရှင်များ:\n\n1. Spider-Man: Across the Spider-Verse\n2. Oppenheimer\n3. Barbie\n4. John Wick 4")

# /download command
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 ဒေါင်းလုဒ်လင့်ရယူရန် ရုပ်ရှင်နာမည်ကို /search နဲ့ ရှာဖွေပါ။\n\nသို့မဟုတ် အောက်ပါလင့်များကို သုံးနိုင်ပါသည်:\n- Example Link 1\n- Example Link 2")

# /stream command
async def stream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 တိုက်ရိုက်ကြည့်ရှုရန် လင့်များ:\n\nhttps://example.com/watch/1\nhttps://example.com/watch/2\n\n(စစ်မှန်သောလင့်များ ထည့်သွင်းပေးပါမည်။)")

# Callback query handler (ပြင်ဆင်ပြီး)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # ==================== ACTION ရုပ်ရှင်များ ====================
    if query.data == "action":
        keyboard = [
            [InlineKeyboardButton("🔥 John Wick 4", callback_data="johnwick4")],
            [InlineKeyboardButton("⚡ Mission Impossible 7", callback_data="mi7")],
            [InlineKeyboardButton("💪 The Equalizer 3", callback_data="equalizer3")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎬 Action ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "johnwick4":
        await query.message.reply_text("🎬 **John Wick 4** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/johnwick4\n\n👆 အပေါ်က လင့်ကိုနှိပ်ပြီး ကြည့်ရှုနိုင်ပါတယ်။")
    
    elif query.data == "mi7":
        await query.message.reply_text("🎬 **Mission Impossible 7** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/mi7\n\n👆 အပေါ်က လင့်ကိုနှိပ်ပြီး ကြည့်ရှုနိုင်ပါတယ်။")
    
    elif query.data == "equalizer3":
        await query.message.reply_text("🎬 **The Equalizer 3** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/equalizer3\n\n👆 အပေါ်က လင့်ကိုနှိပ်ပြီး ကြည့်ရှုနိုင်ပါတယ်။")
    
    # ==================== HORROR ရုပ်ရှင်များ ====================
    elif query.data == "horror":
        keyboard = [
            [InlineKeyboardButton("😱 The Nun 2", callback_data="nun2")],
            [InlineKeyboardButton("🔪 Insidious 5", callback_data="insidious5")],
            [InlineKeyboardButton("🧟 Evil Dead Rise", callback_data="evildead")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("😱 Horror ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "nun2":
        await query.message.reply_text("😱 **The Nun 2** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/nun2")
    
    elif query.data == "insidious5":
        await query.message.reply_text("🔪 **Insidious 5** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/insidious5")
    
    elif query.data == "evildead":
        await query.message.reply_text("🧟 **Evil Dead Rise** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/evildead")
    
    # ==================== COMEDY ရုပ်ရှင်များ ====================
    elif query.data == "comedy":
        keyboard = [
            [InlineKeyboardButton("😂 Barbie", callback_data="barbie")],
            [InlineKeyboardButton("🎭 No Hard Feelings", callback_data="nhf")],
            [InlineKeyboardButton("🍄 Super Mario Bros", callback_data="mario")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("😂 Comedy ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "barbie":
        await query.message.reply_text("😂 **Barbie** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/barbie")
    
    elif query.data == "nhf":
        await query.message.reply_text("🎭 **No Hard Feelings** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/nhf")
    
    elif query.data == "mario":
        await query.message.reply_text("🍄 **Super Mario Bros** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/mario")
    
    # ==================== ROMANCE ရုပ်ရှင်များ ====================
    elif query.data == "romance":
        keyboard = [
            [InlineKeyboardButton("💕 Past Lives", callback_data="pastlives")],
            [InlineKeyboardButton("❤️ Anyone But You", callback_data="aby")],
            [InlineKeyboardButton("⭐ A Star is Born", callback_data="star")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("💕 Romance ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "pastlives":
        await query.message.reply_text("💕 **Past Lives** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/pastlives")
    
    elif query.data == "aby":
        await query.message.reply_text("❤️ **Anyone But You** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/aby")
    
    elif query.data == "star":
        await query.message.reply_text("⭐ **A Star is Born** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/star")
    
    # ==================== DRAMA ရုပ်ရှင်များ ====================
    elif query.data == "drama":
        keyboard = [
            [InlineKeyboardButton("💣 Oppenheimer", callback_data="oppenheimer")],
            [InlineKeyboardButton("🌺 Killers of the Flower Moon", callback_data="killers")],
            [InlineKeyboardButton("🐋 The Whale", callback_data="whale")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎥 Drama ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "oppenheimer":
        await query.message.reply_text("💣 **Oppenheimer** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/oppenheimer")
    
    elif query.data == "killers":
        await query.message.reply_text("🌺 **Killers of the Flower Moon** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/killers")
    
    elif query.data == "whale":
        await query.message.reply_text("🐋 **The Whale** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/whale")
    
    # ==================== SCI-FI ရုပ်ရှင်များ ====================
    elif query.data == "scifi":
        keyboard = [
            [InlineKeyboardButton("🏜️ Dune 2", callback_data="dune2")],
            [InlineKeyboardButton("🌊 Avatar 2", callback_data="avatar2")],
            [InlineKeyboardButton("🤖 The Creator", callback_data="creator")],
            [InlineKeyboardButton("➕ Request Movie", callback_data="request_movie")],
            [InlineKeyboardButton("🔙 Back to Genres", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🤖 Sci-Fi ရုပ်ရှင်များ - ကြည့်ချင်တဲ့ ရုပ်ရှင်ကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "dune2":
        await query.message.reply_text("🏜️ **Dune 2** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/dune2")
    
    elif query.data == "avatar2":
        await query.message.reply_text("🌊 **Avatar 2** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/avatar2")
    
    elif query.data == "creator":
        await query.message.reply_text("🤖 **The Creator** ကြည့်ရှုရန် လင့်:\n\n🔗 https://t.me/your_channel/creator")
    
    # ==================== REQUEST MOVIE ====================
    elif query.data == "request_movie":
        await query.message.reply_text("📝 သင်ကြည့်ချင်တဲ့ ရုပ်ရှင်နာမည်ကို /request [နာမည်] နဲ့ ရိုက်ထည့်ပေးပါ။\n\nဥပမာ - /request Avatar 3")
    
    # ==================== BACK & MAIN MENU ====================
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("🎬 Action", callback_data="action"),
             InlineKeyboardButton("😱 Horror", callback_data="horror")],
            [InlineKeyboardButton("😂 Comedy", callback_data="comedy"),
             InlineKeyboardButton("💕 Romance", callback_data="romance")],
            [InlineKeyboardButton("🎥 Drama", callback_data="drama"),
             InlineKeyboardButton("🤖 Sci-Fi", callback_data="scifi")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎭 အမျိုးအစားတစ်ခုခုကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "main":
        keyboard = [
            [InlineKeyboardButton("🎬 Latest Movies", callback_data="latest_movies"),
             InlineKeyboardButton("🔥 Popular", callback_data="popular_movies")],
            [InlineKeyboardButton("🎭 Genres", callback_data="genres_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏠 **Main Menu**\n\nအောက်ပါရွေးချယ်စရာများထဲက တစ်ခုခုကို ရွေးပါ။", reply_markup=reply_markup)
    
    elif query.data == "latest_movies":
        await query.edit_message_text("🆕 ဒီနေ့ထည့်သွင်းထားသော ရုပ်ရှင်အသစ်များ:\n\n1. Deadpool 3\n2. Inside Out 2\n3. Furiosa\n4. Kingdom of the Planet of the Apes\n\n🔙 /movies နှိပ်ပြီး ပြန်သွားနိုင်ပါတယ်။")
    
    elif query.data == "popular_movies":
        await query.edit_message_text("🔥 လူကြိုက်အများဆုံးရုပ်ရှင်များ:\n\n1. Spider-Man: Across the Spider-Verse\n2. Oppenheimer\n3. Barbie\n4. John Wick 4\n\n🔙 /movies နှိပ်ပြီး ပြန်သွားနိုင်ပါတယ်။")
    
    elif query.data == "genres_menu":
        keyboard = [
            [InlineKeyboardButton("🎬 Action", callback_data="action"),
             InlineKeyboardButton("😱 Horror", callback_data="horror")],
            [InlineKeyboardButton("😂 Comedy", callback_data="comedy"),
             InlineKeyboardButton("💕 Romance", callback_data="romance")],
            [InlineKeyboardButton("🎥 Drama", callback_data="drama"),
             InlineKeyboardButton("🤖 Sci-Fi", callback_data="scifi")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎭 **အမျိုးအစားများ** - သင်နှစ်သက်ရာ အမျိုးအစားကို ရွေးပါ။", reply_markup=reply_markup)

# Main function
def main():
    keep_alive()  # Start Flask web server
    app_bot = Application.builder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))
    app_bot.add_handler(CommandHandler("movies", movies))
    app_bot.add_handler(CommandHandler("search", search))
    app_bot.add_handler(CommandHandler("genre", genre))
    app_bot.add_handler(CommandHandler("request", request_movie))
    app_bot.add_handler(CommandHandler("latest", latest))
    app_bot.add_handler(CommandHandler("popular", popular))
    app_bot.add_handler(CommandHandler("download", download))
    app_bot.add_handler(CommandHandler("stream", stream))
    app_bot.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Bot is running...")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
