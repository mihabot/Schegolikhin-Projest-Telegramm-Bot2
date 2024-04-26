import logging
import hashlib
import requests
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включить ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Классы и их функционал
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def fetch_weather(self, location):
        url = f"{self.base_url}appid={self.api_key}&q={location}"
        response = requests.get(url)
        weather_data = response.json()
        weather_description = weather_data['weather'][0]['description']
        return f"Погода в {location}: {weather_description}."


class EventManager:
    def __init__(self):
        self.events = []

    def create_event(self, details):
        self.events.append(details)
        return f"Событие '{details['title']}' добавлено."


class DataAnalyzer:
    def analyze_data(self, data):
        if not data:
            return "Нет данных для анализа."
        numbers = list(map(int, data.split(',')))
        average = sum(numbers) / len(numbers)
        return f"Среднее значение: {average}"


class ImageProcessor:
    def process_image(self, image_path, output_path):
        with Image.open(image_path) as img:
            filtered_image = img.convert("L")
            filtered_image.save(output_path)
        return "Изображение обработано и сохранено."


class PaymentProcessor:
    def process_payment(self, amount, user):
        return f"Платеж на сумму {amount} от пользователя {user} обработан."


# Экземпляры классов
weather_service = WeatherService(api_key='YOUR_API_KEY')
event_manager = EventManager()
data_analyzer = DataAnalyzer()
image_processor = ImageProcessor()
payment_processor = PaymentProcessor()


# Команды и обработка взаимодействий
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Погода", callback_data='weather')],
        [InlineKeyboardButton("Событие", callback_data='event')],
        [InlineKeyboardButton("Анализ данных", callback_data='analyze')],
        [InlineKeyboardButton("Оплата", callback_data='payment')],
        [InlineKeyboardButton("Обработать изображение", callback_data='process_image')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Выберите действие:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    if data == 'weather':
        query.edit_message_text(text="Введите город для получения погоды.")
    elif data == 'event':
        query.edit_message_text(text="Введите детали события.")
    elif data == 'analyze':
        query.edit_message_text(text="Введите числа через запятую для анализа.")
    elif data == 'payment':
        query.edit_message_text(text="Введите сумму для оплаты и имя пользователя.")
    elif data == 'process_image':
        query.edit_message_text(text="Загрузите изображение для обработки.")


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if 'погода' in context.user_data:
        weather_info = weather_service.fetch_weather(text)
        update.message.reply_text(weather_info)
    elif 'событие' in context.user_data:
        details = {"title": text}
        event_response = event_manager.create_event(details)
        update.message.reply_text(event_response)
    elif 'анализ' in context.user_data:
        analysis_result = data_analyzer.analyze_data(text)
        update.message.reply_text(analysis_result)
    elif 'оплата' in context.user_data:
        # Эта часть требует дополнительной логики для обработки ввода суммы и пользователя
        payment_response = payment_processor.process_payment(text.split()[0], text.split()[1])
        update.message.reply_text(payment_response)
    elif 'обработать изображение' in context.user_data:
        # Эта часть требует интеграции с методами загрузки и сохранения файлов
        image_response = image_processor.process_image(text, "output_path_here")
        update.message.reply_text(image_response)


def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Создайте Updater и передайте ему токен вашего бота.
    updater = Updater("6763072572:AAFb7hxwEp91T8Z3iJyF9btOw6ZSM_m3iN4", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
