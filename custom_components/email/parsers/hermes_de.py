import logging
import re

from ..const import EMAIL_ATTR_BODY

_LOGGER = logging.getLogger(__name__)
ATTR_HERMES_DE = 'hermes_de'
EMAIL_DOMAIN_HERMES_DE = 'myhermes.de'

# Precompile regex pattern for better performance
TRACKING_NUMBER_PATTERN = re.compile(r'Sendungsnummer\s+(H\d+)')

def parse_hermes_de(email):
    """Parse Hermes DE tracking numbers."""
    tracking_numbers = []

    matches = TRACKING_NUMBER_PATTERN.findall(email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers