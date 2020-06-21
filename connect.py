"""
Networking method to connect to the wifi
"""

import network


def wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)  # create a network object
    if not sta_if.isconnected():  # check if we're good to go
        print('connecting to network...')
        sta_if.active(True)  # enable connection
        sta_if.connect(ssid, password)  # connect with given parameters
        while not sta_if.isconnected():  # wait for connection
            continue
    print('network config:', sta_if.ifconfig())
    return str(sta_if.ifconfig()[0])  # return the local ip we got assigned
