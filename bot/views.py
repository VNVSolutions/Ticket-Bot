import logging
import telebot
import string
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
from telebot import types
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from datetime import datetime
from itertools import zip_longest
from .tasks import process_telegram_update
from .conf import bot
from .models import Conditions
from .models import UserProfile
from .models import ConditionsText


logger = logging.getLogger(__name__)

user_context = {}


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update_data = request.body.decode('utf-8')
            process_telegram_update.delay(update_data)
            logger.info(f"Отримане оновлення з webhook: {update_data}")
            return HttpResponse('')
        except Exception as e:
            logger.error(f"Помилка обробки вебхуку: {str(e)}")


def get_conditions():
    condition = Conditions.objects.first()
    return condition.text if condition else "Немає умов."


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    conditions_text = get_conditions()
    bot.send_message(chat_id, f"Умови конкурсу 👇\n\n{conditions_text}", reply_markup=create_reply_markup())


def create_reply_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton('✅ Прийняти участь ✅'))
    return markup


def get_conditions_text():
    condition = ConditionsText.objects.first()
    return condition


def save_user_profile(user_id, username, name):
    user, created = UserProfile.objects.get_or_create(
        telegram_id=user_id,
        defaults={'username': username, 'name': name}
    )
    if not created:
        user.username = username or user.username
        user.name = name or user.name
        user.save()


@bot.message_handler(func=lambda message: message.text == "✅ Прийняти участь ✅")
def accept_participation(message):
    chat_id = message.chat.id
    username = message.from_user.username
    name = message.from_user.first_name

    condition = get_conditions_text()
    if condition:
        response_text = f"{condition.text}\n\nПосилання: {condition.link}"
    else:
        response_text = "Умови відсутні."

    bot.send_message(chat_id, response_text)

    save_user_profile(chat_id, username, name)