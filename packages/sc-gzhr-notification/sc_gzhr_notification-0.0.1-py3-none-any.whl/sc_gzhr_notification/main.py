# The MIT License (MIT)
#
# Copyright (c) 2023 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

from sc_config import ConfigUtils
from sc_gzhr_notification import PROJECT_NAME, __version__
import argparse
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from .email_utils import EmailUtils


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)

        self._emailUtils = EmailUtils(config=self._config)

        self._receivers = list()
        receivers = self._config.get("email.receiver")
        if receivers is not None and type(receivers) == list:
            self._receivers.extend(receivers)

        self._subject = self._config.get("email.subject")

        self._tag = self._config.get("html.tag")
        self._url = self._config.get("html.url")
        self._host = self._config.get("html.host")
        self._keywords = list()
        keywords = self._config.get("html.keywords")
        if keywords is not None and type(keywords) == list:
            self._keywords.extend(keywords)

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config.as_dict()))

        user_agent = UserAgent()
        headers = {
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/avif,image/webp,"
                      "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Host": self._host,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent.random,
        }
        response = requests.get(self._url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.findAll(self._tag)
        found_target = False
        for link in links:
            link_text = link.text
            if link_text is not None:
                found = True
                content = ""
                for keyword in self._keywords:
                    if keyword not in link_text:
                        found = False
                        break
                    content += keyword

                if found:
                    found_target = found
                    content += self._subject
                    content += " " + link['href']
                    self._emailUtils.send_email(
                        subject=self._subject,
                        receivers=self._receivers,
                        html_content=content,
                    )
        if not found_target:
            logging.getLogger(__name__).info("no target found")
        return 0


def main():
    try:
        parser = argparse.ArgumentParser(description='Python project')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
