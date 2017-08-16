#!/usr/bin/env python3
import logging
from time import time, sleep, strptime
from calendar import timegm
from multiprocessing.dummy import Process
from poloniex import Poloniex
import configparser, sys

logger = logging.getLogger(__name__)

WT = '\033[0m'  # white (normal)
RD = lambda text: '\033[31m' + text + WT  # red
GR = lambda text: '\033[32m' + text + WT  # green
OR = lambda text: '\033[33m' + text + WT  # orange
BL = lambda text: '\033[34m' + text + WT  # blue
PR = lambda text: '\033[35m' + text + WT  # purp
CY = lambda text: '\033[36m' + text + WT  # cyan
GY = lambda text: '\033[37m' + text + WT  # gray

loantoshi = 0.000001

def autoRenewAll(api, toggle=True):
    """ Turns auto-renew on or off for all active loans """
    if toggle:
        toggle = 1
    else:
        toggle = 0
    for loan in api.returnActiveLoans()['provided']:
        if int(loan['autoRenew']) != toggle:
            logger.info('Toggling autorenew for offer %s', str(loan['id']))
            api.toggleAutoRenew(loan['id'])


def UTCstr2epoch(datestr, fmat="%Y-%m-%d %H:%M:%S"):
    """
    - takes UTC date string
    - returns epoch
    """
    return timegm(strptime(datestr, fmat))


class Loaner(object):
    """ Loanbot class [API REQUIRES KEY AND SECRET!]"""

    def __init__(self,
                 api,
                 coins={},
                 maxages={},
                 offsets={},
                 delay=60 * 10,
                 fixedRates={},
                 posBases={}):
        self.api, self.delay, self.coins, self.maxages, self.offsets, self.fixedRates, self.posBases =\
            api, delay, coins, maxages, offsets, fixedRates, posBases
        # Check auto renew is not enabled for current loans
        api.returnActiveLoans()['provided']
        #autoRenewAll(self.api, toggle=False)

    def start(self):
        """ Start the thread """
        self.__process = Process(target=self.run)
        self.__process.daemon = True
        self._running = True
        self.__process.start()

    def stop(self):
        """ Stop the thread """
        self._running = False
        try:
            self.__process.join()
        except Exception as e:
            logger.exception(e)

    def getLoanOfferAge(self, order):
        return time() - UTCstr2epoch(order['date'])

    def cancelOldOffers(self):
        logger.info(GR("Checking Open Loan Offers:----------------"))
        offers = self.api.returnOpenLoanOffers()
        for coin in self.coins:
            if coin not in offers:
                logger.debug("No open %s offers found.", coin)
                continue
            for offer in offers[coin]:
                logger.info("%s|%s:%s-[rate:%s]",
                            BL(offer['date']),
                            OR(coin),
                            RD(offer['amount']),
                            GY(str(float(offer['rate']) * 100) + '%')
                            )
                if self.getLoanOfferAge(offer) > maxages.get(coin):
                    logger.info("Canceling %s offer %s",
                                OR(coin), GY(str(offer['id'])))
                    logger.debug(self.api.cancelLoanOffer(offer['id']))

    def createLoanOffers(self):
        logger.info(GR("Checking for coins to lend:---------------"))
        bals = self.api.returnAvailableAccountBalances()
        if not 'lending' in bals:
            return logger.info(RD("No coins found in lending account"))
        for coin in self.coins:
            if coin not in bals['lending']:
                logger.debug("No available %s in lending", OR(coin))
                continue
            amount = bals['lending'][coin]
            logging.info("%s:%s", coin, str(amount))
            if float(amount) < self.coins[coin]:
                logger.debug("Not enough %s:%s, below set minimum: %s",
                             OR(coin),
                             RD(str(amount)),
                             BL(str(self.coins[coin])))
                continue
            orders = self.api.returnLoanOrders(coin)['offers']
            # The Position of the order used as a base here is now user given
            topRate = float(orders[int(posBases.get(coin))]['rate'])
            price = topRate + (float(offsets.get(coin)) * loantoshi)
            # when the determined rate is under the fixedRate, fixedRate is used instead
            if (price < (float(fixedRates.get(coin)) / 100)):
              logger.info('The price is lower than the fixedRate. Using the fixedRate of ' + str(fixedRates.get(coin)) + ' instead')
              price = float(fixedRates.get(coin)) / 100
            logger.info('Creating %s %s loan offer at %s',
                        RD(str(amount)), OR(coin), GR(str(price * 100) + '%'))
            logger.debug(self.api.createLoanOffer(
                coin, amount, price, autoRenew=0))

    def run(self):
        """ Main loop, cancels 'stale' loan offers, turns auto-renew off on
        active loans, and creates new loan offers at optimum price """
        while self._running:
            try:
                # Check for old offers
                self.cancelOldOffers()
                # Create new offer (if can)
                self.createLoanOffers()
                # show active
                active = self.api.returnActiveLoans()['provided']
                logger.info(GR('Active Loans:-----------------------------'))
                for i in active:
                    logger.info('%s|%s:%s-[rate:%s]-[fees:%s]',
                                BL(i['date']),
                                OR(i['currency']),
                                RD(i['amount']),
                                GY(str(float(i['rate']) * 100) + '%'),
                                GR(i['fees'])
                                )

            except Exception as e:
                logger.exception(e)

            finally:
                # sleep with one eye open...
                for i in range(int(self.delay)):
                    if not self._running:
                        break
                    sleep(1)

if __name__ == '__main__':
    from sys import argv
    logging.basicConfig(
        format='[%(asctime)s]%(message)s',
        datefmt=GR("%H:%M:%S"),
        level=logging.INFO
    )
    logging.getLogger('requests').setLevel(logging.ERROR)
    key, secret = argv[1:3]

    #################-Configure Below-##################################
    ########################

    # read the configuration file
    cfg = configparser.ConfigParser()
    cfg.read("pyLendiex.cfg")

    # This dict defines what coins the bot should worry about
    # The dict 'key' is the coin to lend, 'value' is the minimum amount to lend
    coins = { }
    maxages = { }
    fixedRates = { }
    posBases = { }
    offsets = { }
    for i in cfg.sections():
      if (i != "general"):
        try:
          coins.update({i: float(cfg.get(i, "minAmount"))})
          # Maximum age (in secs or minutes) to let an open offer sit
          if ("m" in cfg.get(i, "maxage")):
            maxages.update({i: float(cfg.get(i, "maxage")[:-1]) * 60})
          else:
            maxages.update({i: float(cfg.get(i, "maxage")[:-1])})
          # the fixedRate is used, when the determined price is under this value
          fixedRates.update({i: float(cfg.get(i, "fixedRate"))})
          # which order position is used as a base? Mostly the first 3-5 are used by bots
          posBases.update({i: int(cfg.get(i, "posBase"))})
          # number of loantoshis to offset from lowest asking rate
          offsets.update({i: int(cfg.get(i, "offset"))})
        except ConfigParser.NoOptionError as e:
          print("Error while prasing config file:" + str(e))
          sys.exit(1)

    # number of seconds between loops
    delay = cfg.get("general", "sleepTime")
    if ("m" in delay):
      delay = float(delay[:-1]) * 60
    else:
      delay = float(delay[:-1])

    ########################
    #################-Stop Configuring-#################################
    loaner = Loaner(Poloniex(key, secret, jsonNums=float),
                    coins, maxages, offsets, delay, fixedRates, posBases)
    loaner.start()
    while loaner._running:
        try:
            sleep(1)
        except:
            loaner.stop()
            break
