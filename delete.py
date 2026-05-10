import asyncio
import sys

# Фикс для работы asyncio на Windows (актуально для Python 3.12-3.14)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    _loop = asyncio.get_event_loop()
except RuntimeError:
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

from pyrogram import Client
from pyrogram.enums import ChatType

# --- КОНФИГУРАЦИЯ ---
# Получите свои API ID и HASH на my.telegram.org
API_ID = 0  # Вставьте ваш API ID (число)
API_HASH = ""  # Вставьте ваш API HASH (строка)
# ---------------------

async def main():
    async with Client("my_account", API_ID, API_HASH) as app:
        print("🤖 Соединение установлено! Начинаю поиск каналов...")
        
        count = 0
        async for dialog in app.get_dialogs():
            # Безопасная проверка архива
            folder = getattr(dialog, "folder_id", 0)
            is_archived = (folder == 1)

            # Выходим только из каналов и супергрупп, которые НЕ в архиве
            if dialog.chat.type in [ChatType.CHANNEL, ChatType.SUPERGROUP] and not is_archived:
                print(f"🚀 Выхожу из: {dialog.chat.title}...")
                try:
                    await app.leave_chat(dialog.chat.id)
                    count += 1
                    await asyncio.sleep(1) # Защита от флуд-фильтра Telegram
                except Exception as e:
                    print(f"❌ Ошибка при выходе из {dialog.chat.title}: {e}")
            else:
                status = "В АРХИВЕ" if is_archived else "ЛИЧКА/ГРУППА"
                print(f"😴 Пропускаю: {dialog.chat.title} ({status})")

        print(f"\n✅ Готово! Удалено каналов: {count}")

if __name__ == "__main__":
    try:
        _loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен пользователем")