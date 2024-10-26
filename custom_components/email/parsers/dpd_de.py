import logging
import re

from ..const import EMAIL_ATTR_BODY

_LOGGER = logging.getLogger(__name__)
ATTR_DPD_DE = 'dpd_de'
EMAIL_DOMAIN_DPD_DE = 'dpd.de'

# Precompile regex pattern for better performance
TRACKING_NUMBER_PATTERN = re.compile(r'(?:parcelno=([A-Z0-9]+)|Paketnummer:\s*([0-9]+))')

def parse_dpd_de(email):
    """Parse DPD DE tracking numbers."""
    tracking_numbers = []

    matches = TRACKING_NUMBER_PATTERN.findall(email[EMAIL_ATTR_BODY])
    for match in matches:
        # Each match is a tuple of groups - take the non-empty group
        tracking_number = next(num for num in match if num)
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers