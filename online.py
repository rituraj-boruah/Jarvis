import requests
import wikipedia
import webbrowser
import smtplib
from email.message import EmailMessage
from decouple import config

# Get API keys if added in .env
WEATHER_API_KEY = config("OPENWEATHER_API_KEY", default="")
NEWS_API_KEY = config("NEWS_API_KEY", default="")

# ----------------------------
# Network Utilities
# ----------------------------
def find_my_id():
    try:
        ip = requests.get('https://api64.ipify.org').text
        return ip
    except Exception:
        return "Unable to fetch IP."

# ----------------------------
# Search & Browsing
# ----------------------------
def search_on_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def search_on_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return "Sorry, no result found on Wikipedia."

def youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# ----------------------------
# Email Sending
# ----------------------------
def send_email(to, subject, message):
    try:
        email_user = config("EMAIL_USER")
        email_pass = config("EMAIL_PASS")

        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False

# ----------------------------
# News Fetching
# ----------------------------
def get_news(topic):
    try:
        if not NEWS_API_KEY:
            return ["News API key not provided"]

        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=3"
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            return ["Error fetching news"]

        headlines = [article['title'] for article in data['articles'][:3]]
        return headlines
    except Exception as e:
        return [f"Error: {e}"]

# ----------------------------
# Weather Forecast
# ----------------------------
def weather_forecast(city):
    try:
        if not WEATHER_API_KEY:
            return None, None, None

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        weather = res['weather'][0]['description']
        temp = f"{res['main']['temp']} °C"
        feels_like = f"{res['main']['feels_like']} °C"
        return weather, temp, feels_like
    except:
        return None, None, None
