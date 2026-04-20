__version__ = (1, 3, 3)

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
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor
# meta banner: https://raw.githubusercontent.com/HikkTutor/photo/main/HikkTutor.png
#------------------------------------------------------
# author: vsakoe
# name: MSG

import os
import json
import re
from datetime import datetime
from .. import loader, utils
from telethon.tl.types import Message, DocumentAttributeVideo, DocumentAttributeAudio
 
 
MEDIA_URL_RE = re.compile(
    r'https?://\S+\.(?:jpg|jpeg|png|webp|gif|mp4)(?:\?[^\s\]]*)?$',
    re.IGNORECASE,
)
DOMAIN_RE = re.compile(r'^[\w.-]+\.[a-zA-Z]{2,}')
 
 
@loader.tds
class MSG(loader.Module):
    """Module for creating preset messages"""
 
    strings = {
        "name": "MSG",
        "msg_not_found": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Message not found.</b>",
        "msg_saved": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Saved as:</b> <code>{title}</code>",
        "msg_saved_img_url": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Saved as:</b> <code>{title}</code>\n<i>Direct URL will be used instead of reply media.</i>",
        "msg_saved_no_media": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Saved as:</b> <code>{title}</code>\n<i>To save media with buttons, add a direct photo/gif/video URL as the last argument.</i>",
        "msg_deleted": "<tg-emoji emoji-id=5368359638511166342>🗑</tg-emoji> <b>Deleted:</b> <code>{title}</code>",
        "all_deleted": "<tg-emoji emoji-id=5368359638511166342>🗑</tg-emoji> <b>All messages deleted.</b> ({count})",
        "list_empty": "<tg-emoji emoji-id=5370741373970453373>🗂</tg-emoji> <b>No saved messages.</b>",
        "overwrite_confirm": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Overwrite?</b>\n<i>{date}, {size}</i>",
        "downloading": "<tg-emoji emoji-id=5368700637439629296>📥</tg-emoji> <b>Downloading...</b>",
        "finalizing": "<tg-emoji emoji-id=5368700637439629296>📥</tg-emoji> <b>Finalizing...</b>",
        "sending": "<tg-emoji emoji-id=5371097093632901300>📤</tg-emoji> <b>Sending...</b>",
        "yes": "✅ Yes",
        "no": "❌ No",
        "delete_all": "🗑️ Delete all",
        "confirm_delete": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Delete {count} {declension}?</b>",
        "no_reply": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Reply to a message first.</b>",
        "no_title": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Specify a name:</b> <code>{p}mss name ...</code>",
        "t1": "1 second ago",   "t2_4": "{n} seconds ago",  "t5": "{n} seconds ago",
        "m1": "1 minute ago",   "m2_4": "{n} minutes ago",  "m5": "{n} minutes ago",
        "h1": "1 hour ago",     "h2_4": "{n} hours ago",    "h5": "{n} hours ago",
        "d1": "1 day ago",      "d2_4": "{n} days ago",     "d5": "{n} days ago",
        "w1": "1 week ago",     "w2_4": "{n} weeks ago",    "w5": "{n} weeks ago",
        "mo1": "1 month ago",   "mo2_4": "{n} months ago",  "mo5": "{n} months ago",
        "half_year": "half a year ago",
        "y1": "1 year ago",     "y2_4": "{n} years ago",    "y5": "{n} years ago",
        "msg_singular": "message",  "msg_2_4": "messages",  "msg_5": "messages",
        "bytes": "{n} bytes",   "kb": "{n:.2f} KB",         "mb": "{n:.2f} MB",
        "error_saving": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Saving error.</b>",
        "help": (
            "<tg-emoji emoji-id=5371047940146105367>📝</tg-emoji> <b>MSG — preset messages</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Button colors</b>\n"
            "<code>[🟩 text, url]</code> — green\n"
            "<code>[🟥 text, url]</code> — red\n"
            "<code>[🟦 text, url]</code> — blue\n"
            "Without emoji — default color.\n\n"
            "<b>Button layout</b>\n"
            "<code>[text, url] [text, url]</code> — same row (max 3)\n"
            "<code>[text, url] | [text, url]</code> — two rows\n\n"
            "<b>Photo via URL</b>\n"
            "Insert a direct link to a photo, gif, video at the end of the command\n\n"
            "<code>{p}mss name [🟩 button1, url] [🟥 button2, url] | [🟦 button3, url] direct media url</code>"
        ),
    }
 
    strings_ru = {
        "_cls_doc": "Модуль для создания заготовленных сообщений",
        "msg_not_found": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Сообщение не найдено.</b>",
        "msg_saved": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Сохранено как:</b> <code>{title}</code>",
        "msg_saved_img_url": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Сохранено как:</b> <code>{title}</code>\n<i>Вместо медиа из реплая будет использована прямая ссылка.</i>",
        "msg_saved_no_media": "<tg-emoji emoji-id=5368344017715108822>✅️</tg-emoji> <b>Сохранено как:</b> <code>{title}</code>\n<i>Чтобы сохранить фото и кнопки вместе, добавь прямую ссылку на медиа в конце команды.</i>",
        "msg_deleted": "<tg-emoji emoji-id=5368359638511166342>🗑</tg-emoji> <b>Удалено:</b> <code>{title}</code>",
        "all_deleted": "<tg-emoji emoji-id=5368359638511166342>🗑</tg-emoji> <b>Все сообщения удалены.</b> ({count})",
        "list_empty": "<tg-emoji emoji-id=5370741373970453373>🗂</tg-emoji> <b>Список пуст.</b>",
        "overwrite_confirm": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Перезаписать?</b>\n<i>{date}, {size}</i>",
        "downloading": "<tg-emoji emoji-id=5368700637439629296>📥</tg-emoji> <b>Скачиваю...</b>",
        "finalizing": "<tg-emoji emoji-id=5368700637439629296>📥</tg-emoji> <b>Завершаю...</b>",
        "sending": "<tg-emoji emoji-id=5371097093632901300>📤</tg-emoji> <b>Отправляю...</b>",
        "yes": "✅ Да",
        "no": "❌ Нет",
        "delete_all": "🗑️ Удалить все",
        "confirm_delete": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Удалить {count} {declension}?</b>",
        "no_reply": "<tg-emoji emoji-id=5371092672230494829>❓</tg-emoji> <b>Ответьте на сообщение для сохранения.</b>",
        "no_title": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Укажи название:</b> <code>{p}mss название ...</code>",
        "t1": "1 секунду назад",    "t2_4": "{n} секунды назад",    "t5": "{n} секунд назад",
        "m1": "1 минуту назад",     "m2_4": "{n} минуты назад",     "m5": "{n} минут назад",
        "h1": "1 час назад",        "h2_4": "{n} часа назад",       "h5": "{n} часов назад",
        "d1": "1 день назад",       "d2_4": "{n} дня назад",        "d5": "{n} дней назад",
        "w1": "1 неделю назад",     "w2_4": "{n} недели назад",     "w5": "{n} недель назад",
        "mo1": "1 месяц назад",     "mo2_4": "{n} месяца назад",    "mo5": "{n} месяцев назад",
        "half_year": "полгода назад",
        "y1": "1 год назад",        "y2_4": "{n} года назад",       "y5": "{n} лет назад",
        "msg_singular": "сообщение","msg_2_4": "сообщения",         "msg_5": "сообщений",
        "bytes": "{n} байт",        "kb": "{n:.2f} КБ",             "mb": "{n:.2f} МБ",
        "error_saving": "<tg-emoji emoji-id=5370562759165514904>❌</tg-emoji> <b>Ошибка сохранения.</b>",
        "help": (
            "<tg-emoji emoji-id=5371047940146105367>📝</tg-emoji> <b>MSG — заготовленные сообщения</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Цвет кнопок</b>\n"
            "<code>[🟩 текст, ссылка]</code> — зелёная\n"
            "<code>[🟥 текст, ссылка]</code> — красная\n"
            "<code>[🟦 текст, ссылка]</code> — синяя\n"
            "Без эмодзи — цвет по умолчанию.\n\n"
            "<b>Расположение кнопок</b>\n"
            "<code>[текст, ссылка] [текст, ссылка]</code> — кнопки в ряд (3 максимум)\n"
            "<code>[текст, ссылка] | [текст, ссылка]</code> — кнопки в 2 ряда\n\n"
            "<b>Фото по ссылке</b>\n"
            "Вставь прямую ссылку на фото, гиф, видео в конце команды <code>{p}msg</code>\n\n"
            "<code>{p}mss название [🟩 кнопка1, url] [🟥 кнопка2, url] | [🟦 кнопка3, url] прямая media url</code>"
        ),
    }
 
    EMOJI_STYLES = {"🟩": "success", "🟥": "danger", "🟦": "primary"}
 
    def __init__(self):
        self.storage_path = "./saved_messages"
        self.data_file = os.path.join(self.storage_path, "messages.json")
        self.messages = self._load_messages()
 
    def _load_messages(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {}
 
    def _save_messages(self):
        os.makedirs(self.storage_path, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)
 
    def _normalize_url(self, url):
        url = url.strip()
        if url.startswith(('http://', 'https://', 'tg://')):
            return url
        if DOMAIN_RE.match(url):
            return 'https://' + url
        return None
 
    def _is_media_url(self, url):
        normalized = self._normalize_url(url)
        return bool(normalized and MEDIA_URL_RE.match(normalized))
 
    def format_message(self, template):
        now = datetime.now()
        return template.replace("{time}", now.strftime("%H:%M:%S")).replace("{date}", now.strftime("%Y-%m-%d"))
 
    def _decl(self, n):
        if n % 10 == 1 and n % 100 != 11:
            return "1"
        if 2 <= n % 10 <= 4 and not (10 <= n % 100 <= 20):
            return "2_4"
        return "5"
 
    def _get_time_ago(self, past_time):
        s = int((datetime.now() - past_time).total_seconds())
        pairs = [
            (60, "t", 1), (3600, "m", 60), (86400, "h", 3600),
            (86400 * 7, "d", 86400), (86400 * 30, "w", 86400 * 7),
            (86400 * 365, "mo", 86400 * 30),
        ]
        for boundary, prefix, divisor in pairs:
            if s < boundary:
                n = max(1, s // divisor)
                if prefix == "mo" and n == 6:
                    return self.strings("half_year")
                return self.strings(f"{prefix}{self._decl(n)}").format(n=n)
        n = max(1, s // (86400 * 365))
        return self.strings(f"y{self._decl(n)}").format(n=n)
 
    def _get_count_declension(self, count):
        return self.strings(f"msg_{self._decl(count)}" if count != 1 else "msg_singular")
 
    def _get_size_format(self, size):
        if size < 1024:
            return self.strings("bytes").format(n=size)
        if size < 1024 ** 2:
            return self.strings("kb").format(n=size / 1024)
        return self.strings("mb").format(n=size / 1024 ** 2)
 
    def _style_button(self, button, style="default"):
        styles = {"green": "success", "red": "danger", "blue": "primary"}
        if style in styles:
            button["style"] = styles[style]
        return button
 
    def _parse_args(self, args_str):
        img_url = None
        parts = args_str.strip().rsplit(None, 1)
        if len(parts) == 2 and self._is_media_url(parts[1]):
            img_url = self._normalize_url(parts[1])
            args_str = parts[0].strip()
        bracket_pos = args_str.find('[')
        if bracket_pos == -1:
            return args_str.strip(), img_url, ""
        return args_str[:bracket_pos].strip(), img_url, args_str[bracket_pos:].strip()
 
    def _parse_buttons(self, buttons_str):
        if not buttons_str or not buttons_str.strip():
            return None
        rows = []
        for section in buttons_str.split('|'):
            found = re.findall(r'\[([^\],]+),\s*([^\]]+)\]', section)
            if not found:
                continue
            row = []
            for btn_text, btn_url in found:
                btn_text = btn_text.strip()
                normalized = self._normalize_url(btn_url)
                if not normalized:
                    continue
                btn = {"text": btn_text, "url": normalized}
                for emoji, style in self.EMOJI_STYLES.items():
                    if btn_text.startswith(emoji):
                        btn["style"] = style
                        btn["text"] = btn_text[len(emoji):].strip()
                        break
                row.append(btn)
                if len(row) == 3:
                    rows.append(row)
                    row = []
            if row:
                rows.append(row)
        return rows if rows else None
 
    async def EmojiInline(self, text, message, reply_markup, photo=None):
        form_kwargs = {"text": text, "message": message, "reply_markup": reply_markup}
        if photo:
            form_kwargs["photo"] = photo
        form = await self.inline.form(**form_kwargs)
        try:
            edit_kwargs = {"text": text, "reply_markup": reply_markup}
            if photo:
                edit_kwargs["photo"] = photo
            await form.edit(**edit_kwargs)
        except Exception:
            pass
        return form
 
    @loader.command(ru_doc=" - выводит заготовленное сообщение в чат")
    async def msg(self, message: Message):
        """Send a preset message"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("msg_not_found"))
            return
 
        stored = self.messages.get(args)
        if not stored:
            await utils.answer(message, self.strings("msg_not_found"))
            return
 
        text = self.format_message(stored.get('text', ''))
        buttons = stored.get('buttons')
        media_path = stored.get('media')
        img_url = stored.get('img_url')
 
        if buttons:
            await self.EmojiInline(
                text=text,
                message=message,
                reply_markup=buttons,
                photo=img_url,
            )
        elif img_url:
            await self.client.send_file(message.chat_id, img_url, caption=text, parse_mode="html")
            await message.delete()
        elif media_path and os.path.exists(media_path):
            if os.path.getsize(media_path) > 3 * 1024 * 1024:
                await utils.answer(message, self.strings("sending"))
            await self.client.send_file(message.chat_id, media_path, caption=text, parse_mode="html")
            await message.delete()
        else:
            await utils.answer(message, text)
 
    @loader.command(ru_doc=" - выводит список сохранённых сообщений")
    async def msi(self, message: Message):
        """Show list of saved messages"""
        if not self.messages:
            await utils.answer(message, self.strings("list_empty"))
            return
 
        lines = []
        for title, data in self.messages.items():
            saved_time = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
            size = self._get_size_format(data.get('size', len(data.get('text', '').encode('utf-8'))))
            if data.get('img_url') or (data.get('media') and not data.get('is_audio')):
                emoji = "<tg-emoji emoji-id=5368703785650656375>👁</tg-emoji>"
            elif data.get('is_audio'):
                emoji = "<tg-emoji emoji-id=5375084298871281281>🎤</tg-emoji>"
            else:
                emoji = "<tg-emoji emoji-id=5371047940146105367>📝</tg-emoji>"
            lines.append(f"{emoji} <code>{title}</code>: {size}, {self._get_time_ago(saved_time)}")
 
        await self.EmojiInline(
            text=f"<blockquote expandable>{chr(10).join(lines)}</blockquote>",
            message=message,
            reply_markup=[[
                self._style_button({"text": self.strings("delete_all"), "callback": self.confirm_delete_all}, "red")
            ]],
        )
 
    async def confirm_delete_all(self, call):
        count = len(self.messages)
        await call.edit(
            text=self.strings("confirm_delete").format(count=count, declension=self._get_count_declension(count)),
            reply_markup=[[
                self._style_button({"text": self.strings("yes"), "callback": self.delete_all_messages}, "green"),
                self._style_button({"text": self.strings("no"), "callback": self.close_message}, "red"),
            ]],
        )
 
    async def delete_all_messages(self, call):
        count = len(self.messages)
        for data in self.messages.values():
            mp = data.get('media')
            if mp and os.path.exists(mp):
                os.remove(mp)
        self.messages.clear()
        self._save_messages()
        await call.edit(text=self.strings("all_deleted").format(count=count))
 
    async def close_message(self, call):
        await call.delete()
 
    @loader.command(ru_doc=" - сохраняет сообщение для вывода")
    async def mss(self, message: Message):
        """Save a message for later use"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
 
        if not args:
            await utils.answer(message, self.strings("msg_not_found"))
            return
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return
 
        title, img_url, buttons_str = self._parse_args(args)
 
        if not title:
            await utils.answer(message, self.strings("no_title").format(p=self.get_prefix()))
            return
 
        text = reply.text or ""
        manual_buttons = self._parse_buttons(buttons_str)
 
        if title in self.messages:
            stored = self.messages[title]
            size_saved = self._get_size_format(stored.get('size', len(stored.get('text', '').encode('utf-8'))))
            await self.EmojiInline(
                text=self.strings("overwrite_confirm").format(date=stored['date'], size=size_saved),
                message=message,
                reply_markup=[[
                    self._style_button({
                        "text": self.strings("yes"),
                        "callback": self.overwrite_message,
                        "args": (title, text, reply, manual_buttons, img_url),
                    }, "green"),
                    self._style_button({"text": self.strings("no"), "callback": self.close_message}, "red"),
                ]],
            )
        else:
            await self.save_message(message, title, text, reply, manual_buttons, img_url)
 
    async def overwrite_message(self, call, title, text, reply, manual_buttons, img_url):
        await self.save_message(call, title, text, reply, manual_buttons, img_url)
 
    async def save_message(self, message, title, text, reply, manual_buttons=None, img_url=None):
        try:
            media_path = None
            progress_message = None
            is_audio = False
            has_reply_media = bool(reply and reply.media)
 
            if has_reply_media and not manual_buttons:
                if reply.file.size > 3 * 1024 * 1024:
                    progress_message = await utils.answer(message, self.strings("downloading"))
 
                os.makedirs(self.storage_path, exist_ok=True)
                ext = '.unknown'
                if reply.photo:
                    ext = ".jpg"
                elif reply.document:
                    for attr in reply.document.attributes:
                        if isinstance(attr, DocumentAttributeVideo):
                            ext = ".mp4"
                            break
                        elif isinstance(attr, DocumentAttributeAudio):
                            ext = ".mp3"
                            is_audio = True
                            break
                    else:
                        ext = os.path.splitext(reply.file.name)[1] if reply.file.name else '.unknown'
 
                media_path = os.path.join(self.storage_path, f"{title}_{reply.id}{ext}")
                size = reply.file.size
                await self.client.download_media(reply.media, file=media_path)
 
                if progress_message:
                    await progress_message.edit(self.strings("finalizing"))
            else:
                size = len(text.encode('utf-8'))
 
            self.messages[title] = {
                "text": text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "media": media_path,
                "size": size,
                "is_audio": is_audio,
                "buttons": manual_buttons,
                "img_url": img_url,
            }
            self._save_messages()
 
            if manual_buttons and has_reply_media and img_url:
                msg_key = "msg_saved_img_url"
            elif manual_buttons and has_reply_media and not img_url:
                msg_key = "msg_saved_no_media"
            else:
                msg_key = "msg_saved"
 
            if progress_message:
                await progress_message.edit(self.strings(msg_key).format(title=title))
            else:
                await utils.answer(message, self.strings(msg_key).format(title=title))
        except AttributeError:
            await utils.answer(message, self.strings("error_saving"))
 
    @loader.command(ru_doc=" - удаляет сохранённое сообщение")
    async def msd(self, message: Message):
        """Delete a saved message"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("msg_not_found"))
            return
 
        if args in self.messages:
            mp = self.messages[args].get('media')
            if mp and os.path.exists(mp):
                os.remove(mp)
            del self.messages[args]
            self._save_messages()
            await utils.answer(message, self.strings("msg_deleted").format(title=args))
        else:
            await utils.answer(message, self.strings("msg_not_found"))
 
    @loader.command(ru_doc=" - справка")
    async def msh(self, message: Message):
        """Show help"""
        await utils.answer(message, self.strings("help").format(p=self.get_prefix()))
 
