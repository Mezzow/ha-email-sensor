import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_AMAZON_DE = 'amazon_de'
EMAIL_DOMAIN_AMAZON_DE = 'amazon.de'

# compile regex patterns
BODY_ORDER_PATTERNS = re.compile(r'(?:Order|Bestellnummer): #(.*?)\n')
SUBJECT_ORDER_PATTERNS = re.compile(
    r'Your Amazon\.de order of (.*?) has been dispatched!|'
    r'Deine Amazon\.de-Bestellung mit (.*?) wurde versandt!'
)
TRACK_PACKAGE_PATTERNS = re.compile(
    r'track your package|lieferung verfolgen',
    re.IGNORECASE
)

def parse_amazon_de(email):
    """Parse Amazon tracking numbers."""
    tracking_numbers = []
 

    # see if it's an shipped order email
    order_number_match = BODY_ORDER_PATTERNS.search(email[EMAIL_ATTR_BODY])
    if not order_number_match:
        order_number_match = SUBJECT_ORDER_PATTERNS.search(email[EMAIL_ATTR_SUBJECT])
    if not order_number_match:
        return tracking_numbers

    order_number = order_number_match.group(1)
    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # find the link that has 'track your package' text
    link_elements = soup.find_all('a')
    for link_element in link_elements:
        if not TRACK_PACKAGE_PATTERNS.search(link_element.text):
            continue
        # if found we no get url and check for duplicates
        link = link_element.get('href')

        # make sure we dont have dupes
        order_numbers = list(map(lambda x: x['tracking_number'], tracking_numbers))
        if order_number not in order_numbers:
            tracking_numbers.append({
                'link': link,
                'tracking_number': order_number
            })

    return tracking_numbers