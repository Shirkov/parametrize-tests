from pydantic import BaseModel


class MostroPim(BaseModel):
    host: str
    url: str
    login: str
    password: str


class Search(BaseModel):
    host: str
    url: str
    login: str
    password: str
    engine: str


class MostroSearchSync(BaseModel):
    host: str
    url: str
    login: str
    password: str


class Sync(BaseModel):
    host: str
    url: str
    login: str
    password: str


class Telegram(BaseModel):
    bot_url: str
    token: str
    chat_id: str


class Converter(BaseModel):
    mostro_pim: MostroPim
    search: Search
    mostro_search_sync: MostroSearchSync
    sync: Sync
    telegram: Telegram
