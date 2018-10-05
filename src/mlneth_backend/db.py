#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from config import *
import datetime
from pathlib import Path



class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DB_PATH)


class Banner(BaseModel):
    id = IntegerField(primary_key=True)  # banner ID
    x1 = IntegerField()
    y1 = IntegerField()
    x2 = IntegerField()
    y2 = IntegerField()
    src = CharField()
    local_path = CharField(default='')
    href = CharField()
    alt = CharField()
    block_number = IntegerField()
    transaction_index = IntegerField()
    error = CharField(default='')


class BigPicture(BaseModel):
    BID = IntegerField()  # banner ID
    src = CharField()
    local_path = CharField()
    html = CharField()
    is_serving = BooleanField(default=False)
    error = CharField(default='')

    class Meta:
        auto_increment = False

data = [
    {'id': 66, 'x1': 50, 'y1': 45, 'x2': 52, 'y2': 39, 'src': 'https://imgur.com/6cULacW', 'href': 'https://www.Coinmama.com/?ref=hamster9114', 'alt': 'BUY BITCOINS WITH CREDIT CARD OR CASH! IN MINUTES! @ COINMAMA.com'},
    {'id': 67, 'x1': 50, 'y1': 32, 'x2': 53, 'y2': 38, 'src': '<a href="https://www.CoinMama.com/?ref=hamster9114"><img src="https://www.coinmama.com/assets/img/banners/coinmama_300250_2.jpg" alt="CoinMama: Buy Bitcoins with Credit Card" /></a>', 'href': 'https://www.Coinmama.com/?ref=hamster9114', 'alt': 'BUY BITCOINS WITH CREDIT CARD OR CASH! IN MINUTES! @ Coinmama.com'},
    {'id': 68, 'x1': 50, 'y1': 32, 'x2': 53, 'y2': 38, 'src': 'https://imgur.com/uM53BPF', 'href': 'https://www.Coinmama.com/?ref=hamster9114', 'alt': 'BUY BITCOINS WITH CREDIT CARD OR CASH! IN MINUTES! @ Coinmama.com '},
    {'id': 69, 'x1': 50, 'y1': 39, 'x2': 53, 'y2': 45, 'src': 'https://imgur.com/d56juk6', 'href': 'https://www.Coinmama.com/?ref=hamster9114', 'alt': 'BUY BITCOINS WITH CREDIT CARD OR CASH! IN MINUTES! @ COINMAMA'},
]

class DataBase():

    def __init__(self):
        # my_file = Path("/path/to/file")
        # if !(my_file.is_file()):
        self.db = SqliteDatabase(DB_PATH)
        self.db.connect()
        self.db.create_tables([BigPicture])
        self.db.create_tables([Banner])
        # todo create 0 big_pic

    def write_events(self, safe_events):
        Banner.insert_many(safe_events).execute()

    def get_new_banners(self):
        banners = Banner.select(). \
            where((Banner.local_path == '') & (Banner.error == '')). \
            order_by(Banner.id). \
            limit(MAX_QUERRY_SIZE)
        return banners

    def update_local_image(self, banner, local_path, error):
        banner.local_path = local_path
        banner.error = error
        banner.save()

    # # TODO check if works without autoincrement
    # def get_last_bp(self):
    #     # return 0
    #     bp = BigPicture.select().order_by(BigPicture.BID.desc())
    #     if bp:
    #         return bp.get()
    #     else:
    #         return 0

    def get_banners_from_id(self, from_id):
        banners = Banner.select(). \
            where((Banner.id > from_id) & (Banner.error == '')). \
            order_by(Banner.id). \
            limit(MAX_QUERRY_SIZE)
        return banners

    def get_all_banners(self):
        # todo limit 10000 - wrong. they will not necessarily fill the whole screen
        return Banner.select().where((Banner.id > 0) & (Banner.error == '')).order_by(-Banner.id).limit(10000)

    def close(self):
        self.db.close()


def main():
    data_base = DataBase()
    # data_base.write_events(data)
    print(data_base.get_download_links_list())
    data_base.close()

if __name__ == '__main__':
    # event_name, from_block, logger
    main()
