import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_AMAZON_DE = 'amazon_de'
EMAIL_DOMAIN_AMAZON_DE = 'amazon.de'

def parse_amazon_de(email):
    _LOGGER.debug(email)
    """Parse Amazon tracking numbers."""
    tracking_numbers = []
 
    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # see if it's an shipped order email
    order_number_match = re.search('Order: #(.*?)\n', email[EMAIL_ATTR_BODY]) or re.search('Bestellnummer: #(.*?)\n', email[EMAIL_ATTR_BODY])
    _LOGGER.debug(order_number_match)
    if not order_number_match:
        order_number_match = re.search('Your Amazon.de order of (.*?) has been dispatched!', email[EMAIL_ATTR_SUBJECT]) or re.search('Deine Amazon.de-Bestellung mit (.*?) wurde versandt!', email[EMAIL_ATTR_SUBJECT])
        _LOGGER.debug(order_number_match)
    if not order_number_match:
        return tracking_numbers

    order_number = order_number_match.group(1)

    # find the link that has 'track your package' text
    link_elements = soup.find_all('a')
    _LOGGER.debug(link_elements)
    for link_element in link_elements:
        if not re.search(r'track your package', link_element.text, re.IGNORECASE) and not re.search(r'lieferung verfolgen', link_element.text, re.IGNORECASE):
            continue
        _LOGGER.debug(link_element)
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