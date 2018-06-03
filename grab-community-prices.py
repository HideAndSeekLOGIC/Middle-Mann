import json
import requests
from collections import defaultdict
from pprint import pprint

backpack_file_name = "test_fine_new.json"


class CommunityPrices(object):

    def __init__(self, key="5aab4d78cf6c7542aa73a1bf"):
        """https: // backpack.tf / api / IGetPrices / v4?key = 5
        aab4d78cf6c7542aa73a1bf"""
        with requests.get(f"https://backpack.tf/api/IGetPrices/v4?key={key}&raw=1") as bp:
            self._raw_stats = bp.json()
            if self._raw_stats["response"]["success"] == 0:
                raise IOError(self._raw_stats["response"]["message"])
            self._items = self._raw_stats["response"]["items"]
            self._time = self._raw_stats["response"]["current_time"]

    def update(self):
        """
        Updates prices using API
        """
        with requests.get(f"https://backpack.tf/api/IGetPrices/"
                          f"v4?key={key}&raw=1&since={self._time}") as uf:
            updated_stats = uf.json()
        for item in updated_stats["response"]["items"]:
            self._items[item] \
                = updated_stats["response"]["items"][item]

    def get_items(self, low_price=0, high_price=None):
        """
        Gets all items within given price range
        :param (float) low_price: Lowest price point, 0 by default
        :param (float) high_price: Highest price point, None by default
        :return: (dict): Dictionary of all items in price range
        """
        nested_dict = lambda: defaultdict(nested_dict)
        range_items = nested_dict()
        for item in self._items:
            # print(item)
            # pprint(self._items[item]["prices"])
            prices = self._items[item]["prices"]
            for quality in prices:
                # print(num)
                # print(type(self._items[item]["prices"]))
                tradeables = prices[quality]
                for tradeable in tradeables:
                    craftables = tradeables[tradeable]
                    for craftable in craftables:
                        # print(craftable)
                        indiv_item = craftables[craftable]
                        if type(indiv_item) is list:
                            price = indiv_item[0]["value_raw"]
                            if price >= low_price and (high_price is None or price <= high_price):
                                range_items[item]["prices"][quality][tradeable][craftable] = indiv_item
                        elif type(indiv_item) is dict:
                            for price_index in indiv_item:
                                price = indiv_item[price_index]["value_raw"]
                                if price >= low_price and (high_price is None or price <= high_price):
                                    range_items[item]["prices"][quality][tradeable][craftable][price_index] \
                                        = indiv_item[price_index]

        return range_items


stoof = CommunityPrices()
pprint(stoof.get_items(3, 10))
