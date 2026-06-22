"""
IELTS ZONE Telegram Bot
Run: python bot.py (requires BOT_TOKEN env var)
"""
import os, sys, json, requests, logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
API_URL = os.environ.get('API_URL', 'https://ieltssayt.vercel.app')
POLL_INTERVAL = 2

if not BOT_TOKEN:
    logging.error("BOT_TOKEN environment variable not set!")
    sys.exit(1)


def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logging.error(f"send_message error: {e}")


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    try:
        r = requests.get(url, params=params, timeout=35)
        return r.json().get('result', [])
    except Exception as e:
        logging.error(f"get_updates error: {e}")
        return []


PHONE_KEYBOARD = {
    'keyboard': [[{'text': '📱 Telefon raqamni ulashish', 'request_contact': True}]],
    'resize_keyboard': True,
    'one_time_keyboard': True
}

MAIN_KEYBOARD = {
    'keyboard': [
        [{'text': '📚 Kunlik so\'z'}, {'text': '📝 Test'}],
        [{'text': '🎤 Speaking savol'}, {'text': '📊 Mening natijalarim'}],
        [{'text': '💎 Premium'}, {'text': '🌐 Saytga o\'tish'}],
    ],
    'resize_keyboard': True
}


def handle_message(chat_id, text, user_data):
    text_lower = text.strip().lower()

    if text_lower == '/start':
        msg = (
            "👋 <b>IELTS ZONE botiga xush kelibsiz!</b>\n\n"
            "Bu bot orqali:\n"
            "📚 <b>Kunlik so'z</b> - har kuni yangi IELTS so'zi\n"
            "📝 <b>Test</b> - reading testlari\n"
            "🎤 <b>Speaking savol</b> - speaking amaliyoti\n"
            "📊 <b>Natijalar</b> - profilingiz statistikasi\n"
            "💎 <b>Premium</b> - premium imkoniyatlar\n\n"
            "Avval telefon raqamingizni ulashing:"
        )
        send_message(chat_id, msg, reply_markup=PHONE_KEYBOARD)
        return

    if text_lower == '📚 kunlik so\'z' or text_lower == 'kunlik so\'z':
        try:
            r = requests.get(f"{API_URL}/api/telegram/daily-word", timeout=10)
            data = r.json()
            if 'word' in data:
                msg = (
                    f"📚 <b>Kunlik IELTS so'zi</b>\n\n"
                    f"<b>{data['word']}</b> — {data['translation']}\n"
                    f"📖 {data['definition']}\n"
                    f"✏️ <i>\"{data['example']}\"</i>\n"
                    f"🏷 #{data.get('category', 'General')}"
                )
            else:
                msg = "Hozircha so'zlar mavjud emas."
        except:
            msg = "Xatolik yuz berdi. Keyinroq urinib ko'ring."
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    elif text_lower == '📝 test' or text_lower == 'test':
        try:
            r = requests.get(f"{API_URL}/reading", timeout=10)
            msg = (
                "📝 <b>Reading testlari</b>\n\n"
                f"Testlarni saytda ishlang: {API_URL}/reading\n\n"
                "Bot orqali test topshirish tez orada qo'shiladi!"
            )
        except:
            msg = "Testlarni yuklashda xatolik."
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    elif text_lower == '🎤 speaking savol' or text_lower == 'speaking savol':
        msg = (
            "🎤 <b>Speaking savol</b>\n\n"
            "<b>Part 1:</b> Do you work or study? What do you like about it?\n\n"
            "<b>Part 2:</b> Describe a person you admire.\n\n"
            "<b>Part 3:</b> How has technology changed communication?\n\n"
            "Javobingizni ovozli yozib jo'nating yoki matn shaklida yozing.\n"
            f"To'liq ro'yxat: {API_URL}/speaking"
        )
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    elif text_lower == '📊 mening natijalarim' or 'natija' in text_lower:
        # Check if user is linked
        if 'user_id' not in user_data:
            msg = (
                "📊 <b>Natijalaringiz</b>\n\n"
                "Natijalarni ko'rish uchun avval telefon raqamingizni ulashing:"
            )
            send_message(chat_id, msg, reply_markup=PHONE_KEYBOARD)
            return
        try:
            r = requests.post(f"{API_URL}/api/telegram/auth", json={
                'telegram_id': str(chat_id)
            }, timeout=10)
            data = r.json()
            if data.get('status') == 'ok':
                msg = (
                    f"📊 <b>Mening natijalarim</b>\n\n"
                    f"👤 Foydalanuvchi: {data['username']}\n"
                    f"⭐ Ball: {data['score']}\n"
                    f"💎 Premium: {'✅ Ha' if data.get('is_premium') else '❌ Yo\'q'}\n\n"
                    f"Batafsil: {API_URL}/profile"
                )
            else:
                msg = "Siz hali ro'yxatdan o'tmagansiz. Saytga o'ting va akkaunt yarating."
        except:
            msg = "Xatolik yuz berdi."
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    elif text_lower == '💎 premium':
        msg = (
            "💎 <b>IELTS ZONE Premium</b>\n\n"
            "<b>Premium imkoniyatlar:</b>\n"
            "✅ Mock Exam (4 section)\n"
            "✅ Progress dashboard\n"
            "✅ AI Writing tekshirish\n"
            "✅ CEFR grammar exercises\n"
            "✅ 100+ qo'shimcha testlar\n"
            "✅ Premium badge\n\n"
            f"<b>Narxi:</b> 50,000 so'm/oy\n\n"
            f"Saytda olish: {API_URL}/premium"
        )
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    elif text_lower == '🌐 saytga o\'tish' or 'sayt' in text_lower:
        msg = f"🌐 <b>IELTS ZONE</b>\n\nSayt: {API_URL}\n\nReading, Listening, Writing, Speaking — barchasi bir joyda!"
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)

    else:
        msg = (
            "Iltimos, quyidagi tugmalardan birini tanlang:\n\n"
            "📚 <b>Kunlik so'z</b> — har kuni yangi IELTS so'zi\n"
            "📝 <b>Test</b> — reading testlari\n"
            "🎤 <b>Speaking savol</b> — speaking amaliyoti\n"
            "📊 <b>Mening natijalarim</b> — profilingiz\n"
            "💎 <b>Premium</b> — premium haqida\n"
            "🌐 <b>Saytga o'tish</b> — IELTS ZONE sayti"
        )
        send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)


def handle_contact(chat_id, phone_number, user_data):
    try:
        r = requests.post(f"{API_URL}/api/telegram/auth", json={
            'telegram_id': str(chat_id),
            'phone': phone_number
        }, timeout=10)
        data = r.json()
        if data.get('status') == 'ok':
            user_data['user_id'] = data.get('username', '')
            msg = (
                "✅ <b>Telefon raqamingiz tasdiqlandi!</b>\n\n"
                f"👤 <b>Foydalanuvchi:</b> {data['username']}\n"
                f"⭐ <b>Ball:</b> {data['score']}\n\n"
                "Endi barcha imkoniyatlardan foydalanishingiz mumkin!"
            )
        else:
            msg = (
                "❌ <b>Akkaunt topilmadi.</b>\n\n"
                f"Iltimos, avval saytda ro'yxatdan o'ting: {API_URL}/register\n"
                "So'ng yana telefon raqamingizni ulashing."
            )
    except Exception as e:
        logging.error(f"Contact auth error: {e}")
        msg = "Xatolik yuz berdi. Keyinroq urinib ko'ring."
    send_message(chat_id, msg, reply_markup=MAIN_KEYBOARD)


def main():
    logging.info("Bot ishlayapti...")
    last_update_id = 0
    user_data = {}

    # Set commands
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={
                'commands': [
                    {'command': 'start', 'description': 'Botni ishga tushirish'}
                ]
            },
            timeout=10
        )
    except:
        pass

    while True:
        try:
            updates = get_updates(offset=last_update_id + 1)
            for update in updates:
                update_id = update.get('update_id', 0)
                if update_id > last_update_id:
                    last_update_id = update_id

                chat_id = None
                text = None

                if 'message' in update:
                    msg = update['message']
                    chat_id = msg.get('chat', {}).get('id')

                    # Contact sharing
                    if 'contact' in msg:
                        contact = msg['contact']
                        phone = contact.get('phone_number', '')
                        handle_contact(chat_id, phone, user_data)
                        continue

                    text = msg.get('text', '')

                if chat_id and text:
                    handle_message(chat_id, text, user_data)

        except KeyboardInterrupt:
            logging.info("Bot to'xtatildi.")
            break
        except Exception as e:
            logging.error(f"Main loop error: {e}")

        import time
        time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    main()