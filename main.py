import telebot
from telebot import types

# توكن البوت الخاص بك
TOKEN = '9131381140:AAHpGjj5IVObjA8MsGc_ZL3vpwd4eQ7EhUo'
bot = telebot.TeleBot(TOKEN)

# روابط صور متحركة (GIFs) تفاعلية جذابة
GIF_WELCOME = "https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif"
GIF_STATUS = "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif"
GIF_ABOUT = "https://media.giphy.com/media5/3o7TKSjRrfIPjeiVyM/giphy.gif"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # إنشاء الأزرار التفاعلية (Inline Keyboard)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_status = types.InlineKeyboardButton("📊 حالة النظام", callback_data='status')
    btn_about = types.InlineKeyboardButton("ℹ️ معلومات البوت", callback_data='about')
    markup.add(btn_status, btn_about)
    
    welcome_text = (
        f"مرحباً بك يا {message.from_user.first_name} في 🤖 *Alomari Monitor Bot*!\n\n"
        "اختر من الأزرار أدناه للتفاعل واستعراض الميزات:"
    )
    
    # إرسال رسالة ترحيبية مع صورة GIF متحركة والأزرار
    bot.send_animation(
        message.chat.id, 
        GIF_WELCOME, 
        caption=welcome_text, 
        parse_mode='Markdown', 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'status':
        status_text = "✅ *النظام يعمل بكفاءة عالية وبدون أي مشاكل!*\nجميع الخوادم مستقرة الآن."
        bot.send_animation(call.message.chat.id, GIF_STATUS, caption=status_text, parse_mode='Markdown')
        bot.answer_callback_query(call.id, "تم تحديث الحالة بنجاح!")
        
    elif call.data == 'about':
        about_text = "ℹ️ *Alomari Monitor Bot*\nمخصص لمراقبة وتسهيل المهام عبر تيليجرام باستخدام أزرار تفاعلية وصور متحركة."
        bot.send_animation(call.message.chat.id, GIF_ABOUT, caption=about_text, parse_mode='Markdown')
        bot.answer_callback_query(call.id, "معلومات البوت")

# تشغيل البوت باستمرار
print("Bot is running...")
bot.infinity_polling()
