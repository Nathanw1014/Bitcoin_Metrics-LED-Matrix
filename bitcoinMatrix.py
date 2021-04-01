#!/usr/bin/env python

import re
import time

import json, requests

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT




def jsonreq(url):
        req = requests.get(url).text
        jsonreq = json.loads(req)
        return jsonreq

def display_matrix():
    #Defaults
    url = "https://mempool.space/"
    display_list = []
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False)
    print("Created device")

    #Continuous loop
    while True:

        #fees
        req = jsonreq(url+"/api/v1/fees/recommended")
        msg_fast = 'Fast: '+str(req["fastestFee"])
        display_list.append(msg_fast)
        msg_30 = "Mid: " + str(req["halfHourFee"])
        display_list.append(msg_30)
        msg_1h = "Slow: " + str(req["hourFee"])
        display_list.append(msg_1h)


        #Blockchain data
        req = jsonreq(url+"/api/blocks/tip/height")
        print(req)
        height = "Height: " + str(req)
        display_list.append(height)

        for item in display_list:
            print(item)
            show_message(device, item, fill="white", font=proportional(TINY_FONT))

        #Clear list for next query
        display_list = []


if __name__ == "__main__":
    try:
        display_matrix()
    except KeyboardInterrupt:
        pass