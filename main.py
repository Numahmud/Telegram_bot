import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string

# --- তোমার দেওয়া নতুন আপডেট করা তথ্য ---
API_TOKEN = '8976678352:AAF8RaVc7nzk-3PjBpqRpzKDo2rDa4H02bY'
ADMIN_GROUP_ID = -1003932572317

bot = telebot.TeleBot(API_TOKEN)

def generate_code():
    return 'REDEEM-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📤 Submit Binance Screenshot", callback_data="submit_ss"))
    bot.send_message(
        message.chat.id, 
        "🎥 আমাদের ভিডিওটি মনোযোগ দিয়ে দেখুন। বাইনান্স থেকে ডলার কেনার পর নিচের বাটনে ক্লিক করে স্ক্রিনশট জমা দিন।", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "submit_ss":
        msg = bot.send_message(call.message.chat.id, "📸 দয়া করে বাইনান্স থেকে ডলার কেনার স্ক্রিনশটটি ছবি হিসেবে পাঠান:")
        bot.register_next_step_handler(msg, process_screenshot)
    elif call.data.startswith("approve_"):
        user_id = call.data.split("_")[1]
        code = generate_code()
        bot.send_message(user_id, f"🎉 আপনার পেমেন্ট এপ্রুভ হয়েছে!\n🔑 আপনার সিক্রেট কোড: `{code}`", parse_mode="Markdown")
        bot.edit_message_caption("✅ Approved and Code Sent!", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data.startswith("reject_"):
        user_id = call.data.split("_")[1]
        bot.send_message(user_id, "❌ আপনার স্ক্রিনশটটি বাতিল করা হয়েছে। সঠিক তথ্য দিয়ে আবার চেষ্টা করুন।")
        bot.edit_message_caption("❌ Rejected!", chat_id=call.message.chat.id, message_id=call.message.message_id)

def process_screenshot(message):
    if message.photo:
        photo_id = message.photo[-1].file_id
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.from_user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.from_user.id}")
        )
        bot.send_photo(
            ADMIN_GROUP_ID, 
            photo_id, 
            caption=f"📩 নতুন স্ক্রিনশট জমা পড়েছে!\n👤 ইউজার: @{message.from_user.username}\n🆔 ID: {message.from_user.id}", 
            reply_markup=markup
        )
        bot.reply_to(message, "⏳ আপনার স্ক্রিনশট জমা হয়েছে! এডমিন ভেরিফাই করে এপ্রুভ করলে আপনি কোডটি পেয়ে যাবেন।")
    else:
        bot.reply_to(message, "⚠️ এটি ছবি নয়। দয়া করে স্ক্রিনশটের ছবি পাঠাবেন।")

bot.infinity_polling()
