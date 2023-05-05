import gspread

CREDENTIALS_FILE = 'creds.json'

gc = gspread.service_account(filename=CREDENTIALS_FILE)
sh = gc.open("ЗАЯВКИ НА SEO ЧЕРЕЗ TG БОТА")

ws = sh.get_worksheet(0)


def add_lead(name, phone):
    ws.append_row([name, phone])
