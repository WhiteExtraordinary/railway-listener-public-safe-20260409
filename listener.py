from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import re
import time

api_id_raw = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
string_session = os.getenv("TG_STRING_SESSION")

if not api_id_raw or not api_hash:
    raise RuntimeError("Set TG_API_ID dan TG_API_HASH di environment.")

api_id = int(api_id_raw)
session_name = os.getenv("TG_SESSION_NAME", "session_test")
session_dir = os.getenv("TG_SESSION_DIR", ".")
session_base_path = os.path.join(session_dir, session_name)
session_file_path = f"{session_base_path}.session"

if string_session:
    client = TelegramClient(StringSession(string_session), api_id, api_hash)
    session_mode = "string"
else:
    if not os.path.exists(session_file_path):
        raise RuntimeError(
            f"File session tidak ditemukan: {session_file_path}. "
            "Set TG_STRING_SESSION atau upload file .session."
        )
    client = TelegramClient(session_base_path, api_id, api_hash)
    session_mode = f"file:{session_file_path}"


@client.on(events.NewMessage)
async def handler(event):
    now = time.strftime("%H:%M:%S")

    sender = await event.get_sender()
    username = getattr(sender, "username", None)
    if username:
        user_display = f"@{username}"
    else:
        name = getattr(sender, "first_name", "") or ""
        user_display = name.strip() if name else "unknown"

    if event.is_group or event.is_channel:
        chat = await event.get_chat()
        chat_name = getattr(chat, "title", "unknown")
    else:
        chat_name = None

    flags = []
    if event.is_reply:
        flags.append("REPLY")
    if event.forward:
        flags.append("FWD")

    if event.photo:
        flags.append("PHOTO")
    elif event.video:
        duration = getattr(event.video, "duration", None)
        flags.append(f"VIDEO {duration}s" if duration else "VIDEO")
    elif event.gif:
        flags.append("GIF")
    elif event.document:
        mime = getattr(event.document, "mime_type", "")
        if mime and "video" in mime:
            flags.append("VIDEO")
        else:
            flags.append("DOC")
    elif event.media:
        flags.append("MEDIA")

    text = event.raw_text or ""
    if "http" in text:
        flags.append("LINK")
    if re.search(r"#\w+", text):
        flags.append("HASHTAG")

    flag_str = f"({' '.join(flags)})" if flags else ""
    if chat_name:
        print(f"[{now}] | {chat_name} | {user_display} | {flag_str} {text}")
    else:
        print(f"[{now}] | {user_display} | {flag_str} {text}")


print(f"START listener | session_mode={session_mode}")
client.start()
client.run_until_disconnected()
