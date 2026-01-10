import telebot
import requests
from telebot import types

# --- الإعدادات ---
TELEGRAM_TOKEN = '8306985782:AAGQsbJm2bcKQMVyOq7S09TzP4irfK8exhE'
SUPABASE_URL = "https://abojjjpsjdgcibfceugk.supabase.co/functions/v1/chat"
API_KEY = "worm_e7bCq1CWQOd7orpXQmiDPQmsLYqzhiRO"

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="Markdown")

# دالة معالجة الطلب من الذكاء الاصطناعي (موحدة)
def process_ai_request(message, text):
    bot.send_chat_action(message.chat.id, 'typing')
    payload = {"api_key": API_KEY, "message": text, "session_id": str(message.chat.id)}
    try:
        response = requests.post(SUPABASE_URL, json=payload, timeout=45)
        if response.status_code == 200:
            reply = response.json().get("response", "❌ لم أستطع الرد.")
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, "⚠️ السيرفر مشغول.")
    except:
        bot.reply_to(message, "❌ خطأ في الاتصال.")

# 1. استقبال البيانات من واجهة الويب (Web App)
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    user_text = message.web_app_data.data
    process_ai_request(message, user_text)

# 2. استقبال الرسائل النصية العادية
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # استبدل الرابط أدناه برابط ملف HTML الذي رفعته
        web_info = types.WebAppInfo("https://your-link-here.com") 
        markup.add(types.KeyboardButton("🚀 فتح الواجهة المتطورة", web_app=web_info))
        
        bot.send_message(message.chat.id, "🌟 مرحباً بك! استخدم الزر لفتح التصميم أو اكتب هنا مباشرة.", reply_markup=markup)
    else:
        process_ai_request(message, message.text)

print("🚀 البوت والمحرك يعملان معاً...")
bot.infinity_polling()
