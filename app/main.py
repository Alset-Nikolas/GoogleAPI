from sheet.google_sheet import GoogleSheet
from db import init_db
from telegram.bot import Bot


try:
    from settings import CREDENTIALS_FILE, spreadsheet_id, TOKEN, GROUP_ID
except Exception as er:
    print("В настройках проблема (settings.py)", er)
    exit(0)


def start():
    init_db()
    bot = Bot(TOKEN, GROUP_ID)
    g = GoogleSheet(CREDENTIALS_FILE, spreadsheet_id, bot)
    g.run()


if __name__ == "__main__":
    start()
