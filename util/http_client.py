import io
from typing import List
from xml.etree import ElementTree

import requests
from lxml import etree
import constants


def _generate_url(x: str) -> str:
    return f'http://{constants.IP}:{constants.PORT}/{x}'


def download_file(date: str) -> str:
    return requests.get(_generate_url(date)).text


def fetch_dates_with_sensor_data() -> List[str]:
    api_url = _generate_url('api')
    html_response = requests.get(api_url).text[15:]
    parser = etree.HTMLParser()
    dom: ElementTree = etree.parse(io.StringIO(html_response), parser)
    dates = []
    for elt in dom.iter('a'):
        dates.append(elt.attrib['href'][1:])
    return dates
