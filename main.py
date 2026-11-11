import telebot
from telebot import types

TOKEN = '9131381140:AAHpGjj5IVOBjA8MsGc_ZL3vpwd4eQ7EhUo'
bot = telebot.TeleBot(TOKEN)

GIF_WELCOME = "https://media.giphy.com/media/3oKIPNaiaMCws8vWH6/giphy.gif"
GIF_STATUS = "https://media.giphy.com/media/l0H1RnAWxxn0MhOQE/giphy.gif"
GIF_ABOUT = "https://media.giphy.com/media5/3o7TKSjRrFIPjetZao/giphy.gif"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_status = types.InlineKeyboardButton("📊 حالة النظام", callback_data='status')
    btn_about = types.InlineKeyboardButton("ℹ️ معلومات البوت", callback_data='about')
    markup.add(btn_status, btn_about)
    
    welcome_text = (
        f"مرحباً بك يا أخي الكريم 👋\n\n"
        f"أنا بوت المراقبة الذكي الخاص بك، أعمل على مدار الساعة لخدمتك.\n"
        f"اختر أحد الأزرار أدناه للبدء:"
    )
    bot.send_animation(message.chat.id, GIF_WELCOME, caption=welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'status':
        status_text = "🟢 النظام يعمل بكفاءة تامة وعلى مدار الساعة دون أي انقطاع."
        bot.send_animation(call.message.chat.id, GIF_STATUS, caption=status_text)
    elif call.data == 'about':
        about_text = "🤖 Alomari Monitor Bot\nصُمم خصيصاً لمراقبة الخدمات وإدارتها بكفاءة عالية على منصة Render."
        bot.send_animation(call.message.chat.id, GIF_ABOUT, caption=about_text)
    bot.answer_callback_query(call.id)

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
