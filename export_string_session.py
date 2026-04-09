from telethon import TelegramClient
from telethon.sessions import StringSession
import os

api_id_raw = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

if not api_id_raw or not api_hash:
    raise RuntimeError("Set TG_API_ID dan TG_API_HASH dulu.")

api_id = int(api_id_raw)
session_name = os.getenv("TG_SESSION_NAME", "session_test")
session_dir = os.getenv("TG_SESSION_DIR", ".")
session_base_path = os.path.join(session_dir, session_name)
session_file_path = f"{session_base_path}.session"

if not os.path.exists(session_file_path):
    raise RuntimeError(f"Session file tidak ditemukan: {session_file_path}")

client = TelegramClient(session_base_path, api_id, api_hash)
client.connect()
try:
    if not client.is_user_authorized():
        raise RuntimeError("Session file tidak authorized. Login ulang dulu.")
    print(StringSession.save(client.session))
finally:
    client.disconnect()
