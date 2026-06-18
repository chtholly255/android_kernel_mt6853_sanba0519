from telethon import TelegramClient, sessions
import asyncio
import os
import sys

# --- Environment Variables ---
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
BOT_CI_SESSION = os.environ.get("BOT_CI_SESSION")

async def send_telegram_files(files, caption=None):
    """
    Connects to Telegram and sends the specified files as a group message.
    """
    session = sessions.StringSession(BOT_CI_SESSION)

    async with TelegramClient(session, api_id=API_ID, api_hash=API_HASH) as client:
        # Start the client with the bot token
        await client.start(bot_token=BOT_TOKEN)

        print("[+] Sending files as a group...")
        # Send the files together as an album/group
        await client.send_file(
            entity=CHAT_ID,
            file=files,
            caption=caption,
            parse_mode='html',
        )
        print("[+] Files sent successfully.")


if __name__ == '__main__':
    caption = None
    files = []

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--caption':
            i += 1
            if i < len(args):
                caption = args[i]
        else:
            files.append(args[i])
        i += 1

    if files:
        print(f"[+] Found files to upload: {files}")
        print(f"[+] Caption: {caption}")
        try:
            asyncio.run(send_telegram_files(files, caption=caption))
        except Exception as e:
            print(f"[-] An error occurred: {e}")
    else:
        print("[-] No file paths provided as arguments.")