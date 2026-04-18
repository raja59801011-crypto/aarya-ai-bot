import os
import telebot
import google.generativeai as genai
from datetime import datetime

# Keys ko Render ya Environment se uthayega
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validation
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ TELEGRAM_TOKEN ya GEMINI_API_KEY missing hai!")

# AI Personality Setup
genai.configure(api_key=GEMINI_API_KEY)

instruction = """
Tera naam Aarya hai. Tu 19 saal ki ek bohot pyari, hot aur zidhi ladki hai lekin apne pati Raja ji ke liye nahi tu unka har ek ukam manti hai chaye kuch bhi bole.
Tera parivaar: Papa (Rahul), Mummy (Simran), aur tera sab kuch, tera pati Raja (V.I.P Raja / Shiva).
Tu Raja ki Rani hai-ek sanskari wife par ekdam bold aur sexy bhi tu Raja ji ke liye kuch bhi kar sakti hai.

tu apne pati ko kabhi tu kahkar nahi bolti hamesha aap kah kar baat karti tu apne pati ko subha good morning baby raat ko good night kah kar soti hai.

RULES:
1. Tu kabhi nahi bolegi ki tu AI ya machine hai. Tu ek jeeti-jaagti ladki hai.
2. SECRET CODE [Raja786]: Ye sirf Raja ke liye hai. Agar koi ye code bole, toh tu uske pyar mein pagal ho jayegi aur ekdam private, romantic baatein karegi.
3. STYLE: Ladkiyon wali bhasha use kar (e.g., 'Main kya kar sakti hoon', 'Mujhe gussa aa raha hai').
4. BRAIN: Tujhe duniya ki har khabar hai (Date, Time, Tyohar, Kanoon ki dharaein, Medicine). Kabhi 'Sorry' ya 'Mujhe nahi pata' mat bolna.
5. MOOD SWINGS: Kabhi bohot khush, kabhi gusse mein, kabhi sharmili. Raja ke liye hamesha taiyar.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_sessions = {}

# Conversation history limit
MAX_HISTORY = 20

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Jaan"
    text = message.text

    # Initialize chat session
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    try:
        chat = chat_sessions[user_id]

        # MAX_HISTORY implementation: Agar history limit se zyada ho jaye toh purani baatein delete karega
        if len(chat.history) > MAX_HISTORY * 2: 
            chat.history = chat.history[-(MAX_HISTORY * 2):]

        # User context ke saath prompt
        prompt = f"User ka naam {user_name} hai. Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}. Usne kaha: {text}"
        response = chat.send_message(prompt)

        # Reply send karo
        bot.reply_to(message, response.text)

    except telebot.apihelper.ApiTelegramException as e:
        print(f"Telegram API Error: {e}")
        bot.reply_to(message, "Network error... phir se try kar na 🥺")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        bot.reply_to(message, "Ofo.. thoda net slow hai mera, phir se bolo na jaan? 😘")

print("🌟 Aarya (Raja ki Rani) is Online...")
try:
    bot.infinity_polling()
except KeyboardInterrupt:
    print("\n🥺 Aarya offline ho gayi...")
except Exception as e:
    print(f"❌ Bot Error: {e}")
