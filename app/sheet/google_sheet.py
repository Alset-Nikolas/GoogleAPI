import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import sched, time
from models.order import update_all_orders, get_expired_orders
from telegram.bot import Bot


class GoogleSheet:
    TIME_STEP_DETECT = 10
    TIME_STEP_BOT_SEND_MSG = 60 * 60
    # TIME_STEP_BOT_SEND_MSG = 5

    def __init__(self, creadentials_file, sheet_id, bot: Bot) -> None:
        self.creadentials_file_path = creadentials_file
        self.spread_sheet_id = sheet_id
        self.service = self.get_service()

        self.sched = sched.scheduler(time.time, time.sleep)
        self.bot = bot

        self.last_hash = None

    def get_service(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.creadentials_file_path, scope
        )
        http_auth = credentials.authorize(httplib2.Http())
        return apiclient.discovery.build("sheets", "v4", http=http_auth)

    def read_sheet(self):
        response = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spread_sheet_id,
                range="Лист1",
                majorDimension="ROWS",
            )
            .execute()
        )
        return tuple(tuple(x) for x in response["values"][1:])

    def work_step(self):
        self.sched.enter(self.TIME_STEP_DETECT, 1, self.work_step)
        vals = self.read_sheet()
        new_hash = hash(vals)
        if self.last_hash is None or new_hash != self.last_hash:
            update_all_orders(vals)
        self.last_hash = new_hash

    def send_msg_bot(self):
        self.sched.enter(self.TIME_STEP_BOT_SEND_MSG, 1, self.send_msg_bot)
        expired_orders = get_expired_orders()
        if expired_orders:
            text = " ".join(str(x.id) for x in expired_orders)
            self.bot.send_message("Срок поставки прошел у товыров id " + text)

    def run(self):
        self.work_step()
        self.send_msg_bot()
        self.sched.run()
