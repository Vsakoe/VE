__version__ = (1, 1, 7)
#            © Copyright 2026
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#------------------------------------------------------
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#------------------------------------------------------
# meta developer: @HikkTutor
# meta banner: https://raw.githubusercontent.com/HikkTutor/photo/main/HikkTutor.png
#------------------------------------------------------
# author: vsakoe
# name: Cping

import time
from datetime import datetime, timedelta
import re
from .. import loader, utils
from telethon.tl.types import Message
import logging
@loader.tds
class Cping(loader.Module):
    """Настраиваемый пинг с поддержкой медиа и премиум эмодзи"""
    strings = {
        "name": "Cping",
        "configping": (
            "Your custom text.\n"
            "You can use arguments:\n"
            "{ping} - Ping (in milliseconds).\n"
            "{up} - System uptime.\n"
            "{time} - Current time.\n"
            "{date} - Current date.\n"
            "{day} - Current day of the week.\n"
            "{ny} - Until the specified date (days or hours).\n"
            "{emoji_line} - Space for your premium emojis.\n"
            "{stat} - Emoji for ping level.\n"
            "{timemoj} - Emoji for time of day.\n\n"
            "Use tags for text formatting:\n"
            "[b]text[/b] - Bold text\n"
            "[m]text[/m] - Monospace text\n"
            "[s]text[/s] - Strikethrough text\n"
            "[u]text[/u] - Underlined text\n\n"
            "If the config is too long, you can use: .fcfg Cping ping your settings\n"
        ),
        "countdown_hint": (
            "Date format for countdown: 'Day Month Time Year'\n"
            "- Examples:\n"
            "  '01 January 12:00 2025' - full date with year and time.\n"
            "  '01 January 12:00' - the year will automatically be added as current or next if the date has passed.\n"
            "  'Friday 15:45' - closest Friday, year and month are not specified.\n"
            "  '14 June' - day and month, time will be 00:00.\n\n"
            "- Specifying time is mandatory, if not specified - it will be 00:00.\n"
            "- If the year is not specified, the current year is used, but if the date has already passed, the next year will be used.\n"
            "- If the day of the week is not specified, the closest day with the specified time is used."
        ),
        "moon_hint": "Emoji at the start of the message (can be empty)",
        "poyas_hint": (
            "Add or subtract hours.\n"
            "For those using paid hosting located outside your timezone\n"
            "-Negative number to subtract hour(s)\n"
            "+Positive number to add hour(s)\n"
        ),
        "media_hint": "Link to media (photo/video/gif) to attach to ping message.",
        "stat_hint": "Emojis for ping levels in format: good|medium|bad",
        "time_emojis_hint": (
            "Emojis to represent time of day, separated by |.\n"
            "Examples:\n"
            "2 emojis: '🌞|🌜' - Day and night\n"
            "3 emojis: '🌅|🌞|🌆' - Morning, day, evening\n"
            "4 emojis: '🌅|🌞|🌆|🌙' - Morning, day, evening, night\n"
            "Any number of emojis can be used, they will be evenly distributed across 24 hours."
        ),
        "lang_hint": "Module language: ru or en",
        "uptime_hint": "Toggle display of detailed uptime (with hours, minutes): on or off",
    }
    strings_ru = {
        "name": "Cping",
        "configping": (
            "Ваш кастомный текст.\n"
            "Вы можете использовать аргументы:\n"
            "{ping} - Пинг (в миллисекундах).\n"
            "{up} - Время работы системы.\n"
            "{time} - Текущее время.\n"
            "{date} - Текущая дата.\n"
            "{day} - Текущий день недели.\n"
            "{ny} - До заданной даты (дни или часы).\n"
            "{emoji_line} - Место для ваших премиум эмодзи.\n"
            "{stat} - Эмодзи уровня пинга.\n"
            "{timemoj} - Эмодзи для времени суток.\n\n"
            "Используйте теги для форматирования текста:\n"
            "[ж]текст[/ж] - Жирный текст\n"
            "[м]текст[/м] - Моноширинный текст\n"
            "[з]текст[/з] - Зачёркнутый текст\n"
            "[п]текст[/п] - Подчёркнутый текст\n\n"
            "Если в кфг не влазит весь текст, то вы можете использовать: .fcfg Cping ping ваши настройки\n"
        ),
        "countdown_hint": (
            "Формат даты для отсчёта: 'Число месяц время год'\n"
            "- Примеры:\n"
            "  '01 января 12:00 2025' - полная дата с годом и временем.\n"
            "  '01 января 12:00' - год будет автоматически добавлен как текущий или следующий, если дата прошла.\n"
            "  'пятница 15:45' - ближайшая пятница, год и месяц не указываются.\n"
            "  '14 июня' - день и месяц, время будет 00:00.\n\n"
            "- Указание времени обязательно, если не указано - будет 00:00.\n"
            "- Если не указан год, используется текущий год, но если дата уже прошла, будет использован следующий год.\n"
            "- Если не указан день недели, используется ближайший день с указанным временем."
        ),
        "moon_hint": "Эмодзи в начале сообщения (может быть пустым)",
        "poyas_hint": (
            "Добавить или отнять часы.\n"
            "Пункт для тех, у кого платный хостинг находящийся за пределами часового пояса\n"
            "-число чтобы отнять час(ы)\n"
            "+число чтобы добавить час(ы)\n"
        ),
        "media_hint": "Ссылка на медиа (фото/видео/гиф), которое будет прикреплено к сообщению с пингом.",
        "stat_hint": "Эмодзи для уровней пинга в формате: хороший|средний|плохой",
        "time_emojis_hint": (
            "Эмодзи для отображения времени суток, разделенные |.\n"
            "Примеры:\n"
            "2 эмодзи: '🌞|🌜' - День и ночь\n"
            "3 эмодзи: '🌅|🌞|🌆' - Утро, день, вечер\n"
            "4 эмодзи: '🌅|🌞|🌆|🌙' - Утро, день, вечер, ночь\n"
            "Можно использовать любое количество эмодзи, они будут распределены равномерно на 24 часа."
        ),
        "lang_hint": "Язык модуля: ru или en",
        "uptime_hint": "Переключение отображения детального времени работы (с часами, минутами): on или off",
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ping",
                (
                    "{emoji_line}\n"
                    "🚀Пинг: {ping} ms {stat}\n"
                    "⏳Аптайм: {up}\n"
                    "⏰Время: {time}, {day}\n"
                    "🗓До нового года: {ny}\n"
                    "{timemoj}\n"
                    "{emoji_line}"
                ),
                lambda: self.strings["configping"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "daytime",
                "1 января 0:00",
                lambda: self.strings["countdown_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "moon",
                "🌘", 
                lambda: self.strings["moon_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "poyas",
                0,
                lambda: self.strings["poyas_hint"],
                validator=loader.validators.Integer(minimum=-12, maximum=14),
            ),
            loader.ConfigValue(
                "media",
                None,
                lambda: self.strings["media_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "stat",
                "🟢|🟡|🔴",
                lambda: self.strings["stat_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "time_emojis",
                "🌅|🌞|🌆|🌜",
                lambda: self.strings["time_emojis_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "lang",
                "ru",
                lambda: self.strings["lang_hint"],
                validator=loader.validators.Choice(["ru", "en"]),
            ),
            loader.ConfigValue(
                "uptime",
                "on",
                lambda: self.strings["uptime_hint"],
                validator=loader.validators.Choice(["on", "off"]),
            ),
        )
    def get_strings(self):
        lang = self.config["lang"]
        if lang not in ["ru", "en"]:
            lang = "ru"
        return self.strings_ru if lang == "ru" else self.strings
    def get_plural(self, number, one, two, five):
        n = abs(number) % 100
        if 11 <= n <= 19:
            return five
        n = n % 10
        if n == 1:
            return one
        elif 2 <= n <= 4:
            return two
        return five
    def parse_date(self, date_str):
        today = datetime.now()
        months = {
            'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
            'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
            'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
        }
        days_of_week = {
            'понедельник': 0, 'вторник': 1, 'среда': 2,
            'четверг': 3, 'пятница': 4, 'суббота': 5, 'воскресенье': 6,
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,
        }
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            pass
        for day_name, day_index in days_of_week.items():
            if day_name in date_str.lower():
                time_part = re.search(r'\d{1,2}:\d{2}', date_str)
                target_date = today + timedelta((day_index - today.weekday() + 7) % 7)
                if time_part:
                    target_time = datetime.strptime(time_part.group(), "%H:%M").time()
                    target_date = target_date.replace(hour=target_time.hour, minute=target_time.minute, second=0)
                if target_date < today:
                    target_date += timedelta(weeks=1)
                return target_date
        match = re.match(r'(\d{1,2})\s+([а-яa-z]+)\s*(\d{4})?\s*(\d{1,2}:\d{2})?', date_str.lower())
        if match:
            day, month_name, year, time_part = match.groups()
            month = months.get(month_name)
            year = int(year) if year else today.year
            target_time = datetime.strptime(time_part, "%H:%M").time() if time_part else datetime.min.time()
            target_date = datetime(year, month, int(day), target_time.hour, target_time.minute)
            if target_date < today:
                target_date = target_date.replace(year=year + 1)
            return target_date
        raise ValueError("Неправильный формат даты")
    def days_to_date(self):
        try:
            countdown_date_str = self.config["daytime"]
            target_date = self.parse_date(countdown_date_str)
            hour_offset = self.config["poyas"]
            today = datetime.now() + timedelta(hours=hour_offset)
            time_difference = target_date - today
            lang = self.config["lang"]
            if lang == "ru":
                if time_difference.total_seconds() < 86400:
                    hours, remainder = divmod(time_difference.seconds, 3600)
                    minutes = remainder // 60
                    return f"{hours} {self.get_plural(hours, 'час', 'часа', 'часов')} и {minutes} {self.get_plural(minutes, 'минута', 'минуты', 'минут')}"
                else:
                    days = time_difference.days
                    return f"{days} {self.get_plural(days, 'день', 'дня', 'дней')}"
            else:
                if time_difference.total_seconds() < 86400:
                    hours, remainder = divmod(time_difference.seconds, 3600)
                    minutes = remainder // 60
                    return f"{hours} {'hour' if hours == 1 else 'hours'} and {minutes} {'minute' if minutes == 1 else 'minutes'}"
                else:
                    days = time_difference.days
                    return f"{days} {'day' if days == 1 else 'days'}"
        except ValueError as e:
            logging.error(f"Ошибка в дате: {e}")
            return "Ошибка в дате"
    def translate_uptime(self, uptime):
        lang = self.config["lang"]
        if lang == "ru":
            translated = uptime.replace("days", "дней").replace("day", "день").replace("hours", "часов").replace("hour", "час")
            return translated
        return uptime
    def format_text(self, text):
        replacements = {
            r"\[b\]": "<b>", r"\[/b\]": "</b>",
            r"\[m\]": "<code>", r"\[/m\]": "</code>",
            r"\[s\]": "<s>", r"\[/s\]": "</s>",
            r"\[u\]": "<u>", r"\[/u\]": "</u>",
            r"\[ж\]": "<b>", r"\[/ж\]": "</b>",
            r"\[м\]": "<code>", r"\[/м\]": "</code>",
            r"\[з\]": "<s>", r"\[/з\]": "</s>",
            r"\[п\]": "<u>", r"\[/п\]": "</u>",
        }
        for key, value in replacements.items():
            text = re.sub(key, value, text, flags=re.IGNORECASE)
        return text
    def get_stat_emoji(self, ping_time):
        emojis = self.config["stat"].split('|')
        if len(emojis) != 3:
            logging.error("Неверный формат конфигурации stat. Используйте формат: хороший|средний|плохой.")
            return "❓"
        if ping_time <= 200:
            return emojis[0]
        elif ping_time <= 600:
            return emojis[1]
        else:
            return emojis[2]
    def get_time_emoji(self, hour, season):
        time_emojis = self.config["time_emojis"].split('|')
        num_emojis = len(time_emojis)
        if num_emojis == 0:
            return ""
        if season == 'summer':
            day_start, evening_start, night_start = 5, 19, 22
        elif season == 'winter':
            day_start, evening_start, night_start = 8, 17, 20
        else:
            day_start, evening_start, night_start = 6, 18, 21
        if num_emojis == 2:
            return time_emojis[0] if day_start <= hour < night_start else time_emojis[1]
        elif num_emojis == 3:
            if day_start <= hour < evening_start:
                return time_emojis[0]
            elif evening_start <= hour < night_start:
                return time_emojis[1]
            else:
                return time_emojis[2]
        elif num_emojis == 4:
            if day_start <= hour < (day_start + (evening_start - day_start) // 2):
                return time_emojis[0]
            elif (day_start + (evening_start - day_start) // 2) <= hour < evening_start:
                return time_emojis[1]
            elif evening_start <= hour < night_start:
                return time_emojis[2]
            else:
                return time_emojis[3]
        else:
            interval = 24 // num_emojis
            index = hour // interval
            return time_emojis[index if index < num_emojis else -1]
    def determine_season(self, month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    def format_uptime(self, uptime):
        if self.config["uptime"] == "off":
            days_match = re.search(r"(\d+) (day|days|день|дней|дня)", uptime)
            if days_match:
                return days_match.group()
        return uptime
    @loader.command(
        ru_doc=" - Узнать пинг вашего юзербота",
        en_doc=" - Check your userbot's ping",
    )
    async def cping(self, message: Message):
        strings = self.get_strings()
        start = time.perf_counter_ns()
        moon = self.config["moon"] or "🌘"
        await utils.answer(message, moon)
        ping_time = round((time.perf_counter_ns() - start) / 10**6, 3)
        uptime = utils.formatted_uptime()
        uptime = self.format_uptime(self.translate_uptime(uptime))
        hour_offset = self.config["poyas"]
        current_time = datetime.now() + timedelta(hours=hour_offset)
        current_time_str = current_time.strftime("%H:%M:%S")
        current_date = current_time.strftime("%Y-%m-%d")
        season = self.determine_season(current_time.month)
        time_emoji = self.get_time_emoji(current_time.hour, season)
        day_of_week = current_time.strftime("%A")
        lang = self.config["lang"]
        if lang == "ru":
            days_of_week = {
                "Monday": "Понедельник",
                "Tuesday": "Вторник",
                "Wednesday": "Среда",
                "Thursday": "Четверг",
                "Friday": "Пятница",
                "Saturday": "Суббота",
                "Sunday": "Воскресенье",
            }
            day_of_week = days_of_week.get(day_of_week, "Неизвестный день")
        days_to_event = self.days_to_date()
        ping_emoji = self.get_stat_emoji(ping_time)
        response = self.config["ping"].format(
            ping=ping_time,
            up=uptime,
            time=f"{current_time_str}",
            timemoj=time_emoji,
            date=current_date,
            day=day_of_week,
            ny=days_to_event,
            emoji_line="",
            moon=moon,
            stat=ping_emoji
        )
        response = self.format_text(response)
        media = self.config["media"]
        
        if media:
            try:
                await utils.answer_file(message, media, caption=response)
            except Exception as e:
                logging.error(f"Ошибка при отправке медиа: {e}")
                await utils.answer(message, response)
        else:
            await utils.answer(message, response)
