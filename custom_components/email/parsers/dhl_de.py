import logging
import re

from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_DHL_DE = 'dhl_de'
EMAIL_DOMAIN_DHL_DE = 'dhl.de'


def parse_dhl_de(email):
    """Parse DHL DE tracking numbers."""
    tracking_numbers = []

    matches = re.findall(r'piececode=(.*?)"', email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers
