import datetime
import locale
import os
import json

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChat


async def main():
    locale.setlocale(locale.LC_ALL, "it_IT")
    waste = get_waste_list()
    if waste is not None:
        await client.send_message(PeerChat(873506392), message=waste)


def get_waste_list():
    with open("raccolta_differenziata.json", "r") as f:
        calendar = json.load(f)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime("%m-%d")
        if tomorrow in calendar:
            return get_formatted_waste(calendar[tomorrow])
        return None


def get_formatted_waste(waste: list[str]) -> str:
    waste = map(lambda x: "* " + x, waste)
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%A %-d %B")
    message = (
        f"Ciao, domani, {tomorrow}, verranno raccolti i seguenti rifiuti:"
        + "\n\n"
        + ("\n".join(waste))
    )
    return message


if __name__ == "__main__":
    api_id = int(os.environ.get("TG_APP_ID"))
    api_hash = os.environ.get("TG_API_HASH")
    session = os.environ.get("TG_SESSION")
    with TelegramClient(StringSession(session), api_id, api_hash) as client:
        client.loop.run_until_complete(main())
