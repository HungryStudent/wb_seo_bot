import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["settings"]["TOKEN"]
OPENAI_TOKEN = config["settings"]["OPENAI_TOKEN"]
BOTNAME = config["settings"]["BOTNAME"]
SUPPORT_BOTNAME = config["settings"]["SUPPORT_BOTNAME"]
ADMINS = config["settings"]["admins"].split(",")
ADMINS = [int(admin) for admin in ADMINS]
pay_token = config["settings"]["pay_token"]

video_file_id = config["file_id"]["video"]
doc_file_id = config["file_id"]["doc"]


class DB:
    user = config["db"]["user"]
    password = config["db"]["password"]
    database = config["db"]["database"]
    host = config["db"]["host"]
    port = config["db"]["port"]
