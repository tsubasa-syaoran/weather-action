import os
import requests
from datetime import datetime, timedelta

def get_weather(city, api_key):
    """获取天气信息"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_cn"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']


        # UTC 时间 + 8 小时 = 北京时间
        beijing_time = datetime.utcnow() + timedelta(hours=8)

        return (
            f"🌤 城市: {city}\n"
            f"⏰ 时间: {beijing_time:%Y-%m-%d %H:%M} (北京时间)\n"
            f"天气: {weather_desc}\n"
            f"温度: {temp}°C (体感 {feels_like}°C)\n"
            f"湿度: {humidity}%\n"
            f"风速: {wind_speed} m/s"
        )
    except Exception as e:
        return f"获取天气失败: {e}"

def send_telegram_message(bot_token, chat_id, text):
    """发送消息到 Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": text})
        resp.raise_for_status()
    except Exception as e:
        print(f"发送 Telegram 消息失败: {e}")

if __name__ == "__main__":
    city = os.getenv("CITY")
    weather_api_key = os.getenv("WEATHER_API_KEY")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([city, weather_api_key, bot_token, chat_id]):
        raise ValueError("缺少必要的环境变量")

    weather_info = get_weather(city, weather_api_key)
    send_telegram_message(bot_token, chat_id, weather_info)
