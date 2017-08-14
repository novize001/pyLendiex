# pyPoloniexLender
Poloniex cryptocurrency lending bot. The bot works with the interface provided by s4w3d0ff and is originally based on an example provided made by s4w3d0ff: https://github.com/s4w3d0ff/python-poloniex

# What's new with this bot
This bot uses the Python API bindings, which were created by the user s4w3d0ff. This bot includes two major advantages:

1. Lending of any coin which is allowed to be lended on Poloniex.
2. A central config file to set a couple of option per coin like the minimum amount to lend, a fixed rate and so on.
3. Setting the interval when the bot should repeat it's work.

# How to use it
Basically you have to install the Python interface from s4w3d0ff. You can find a installation instruction on their GitHub (see link above). After you've done this, you can download the latest release of the pyPoloniexLender. Before you start the Lender you have to configure the loanbot.cfg file and edit it to your needs (this file includes full comments for every single option). Then you can start the bot like this:
```
python loanbot.py myPoloniexAPI myPoloniexSecret
```

# Thanks
Shout out to the fantastic Poloniex API, written by s4w3d0ff!

If you want to give a small tip, use the following addresses:
* BTC: 19569fzZYUBAfvyHwuux4bgeyuqX8b7ZYR
* DOGE: tba
* RDD: RqwxsQvmoKZ8hgjgrcEZF2CEGsocp4ziXi
