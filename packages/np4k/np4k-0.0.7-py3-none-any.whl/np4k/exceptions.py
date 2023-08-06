

"""
paywall exceptions
case 1: article only half parses due to paywall (e.g. for NYT)
case 2: article doesn't parse at all due to paywall and has "are you a robot msg" or something similar (e.g. for Bloomberg, ft)
case 3: article doesn't parse at all due to paywall and no message (not where this is)
"""


class PaywallException(Exception):
    def __init__(self, message: str = "Partial paywall detected"):
        self.message = message
        super().__init__(self.message)

