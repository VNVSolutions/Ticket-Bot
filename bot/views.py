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


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) > 1 and args[1] == 'participate':
        condition = get_conditions_text()
        if condition:
            response_text = f"{condition.text}\n\nДякуємо за участь!"
        else:
            response_text = "Умови відсутні."

        bot.send_message(chat_id, response_text)
        save_user_profile(chat_id, message.from_user.username, message.from_user.first_name)
    else:
        bot.send_message(chat_id, f"Ви вже берете участь!")


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
