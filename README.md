# pyLendiex
Poloniex cryptocurrency lending bot. The bot works with the interface provided by s4w3d0ff and is originally based on an example provided made by s4w3d0ff: https://github.com/s4w3d0ff/python-poloniex
pyLendiex is only compatible with Python3!

# What's new with this bot
This bot uses the Python API bindings, which were created by the user s4w3d0ff. This bot includes two major advantages:

1. Lending of any coin which is allowed to be lended on Poloniex.
2. A central config file to set a couple of option per coin like the minimum amount to lend, a fixed rate and so on.
3. Setting the interval when the bot should repeat it's work.

However, this bot is dump. It's only doing what the user says him to do so. Use it at your own risk!

# How to use it
Basically you have to install Python3, the Python configparser. For e.g. under Ubuntu / Debian this would look like this:
```
sudo apt-get install python3 python3-pip python-configparser
```
You also need the Python API Poloniex bindings from s4w3d0ff. You can find a installation instruction on their GitHub (see link above). After you've done this, you can download the latest release of the pyLendiex. Before you start the Lender you have to configure the loanbot.cfg file and edit it to your needs (this file includes full comments for every single option). Then you can start the bot like this:
```
python pyLendiex.py myPoloniexAPI myPoloniexSecret
```
You can find a further installation manual for Ubuntu, Debian and Raspbian here: http://www.mybitcoin.space/2017/08/pylendiex-v01-released.html

# Thanks
Shout out to the fantastic Poloniex API bindings, written by s4w3d0ff!

If you want to give a small tip, use the following addresses:
* BTC: 19569fzZYUBAfvyHwuux4bgeyuqX8b7ZYR
* DOGE: DNeLigQypCiKJh32EppngbR6M5jsnJD5aM
* RDD: RqwxsQvmoKZ8hgjgrcEZF2CEGsocp4ziXi
