import strategy
import scapy.all as scapy
import logging
import re

logger = logging.getLogger(__name__)

class PassiveStrategy(strategy.Strategy):
    needsip = False
    challenge = 'listen'

    def execute(self, runner):
        def examine(pkt):
            logger.debug(pkt.sprintf("{IP:%IP.src%: }{Raw:%Raw.load%}"))

            if pkt.haslayer(scapy.Raw):
                try:
                    load = pkt.load.decode('utf-8')
                except DecodeError:
                    return

                m = re.search(runner.flagpattern, load)
                if m:
                    raise strategy.FlagFound(m.group(0))

        try:
            scapy.sniff(iface=runner.iface, filter='udp', prn=examine)
        except strategy.FlagFound as exp:
            return exp.flag
        else:
            raise strategy.Abort("Sniffer exited without finding flag")
