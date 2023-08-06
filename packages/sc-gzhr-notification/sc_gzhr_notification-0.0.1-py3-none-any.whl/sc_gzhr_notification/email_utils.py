# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2023 Scott Lau <exceedego@126.com>
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
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config42 import ConfigManager


class EmailUtils:

    def __init__(self, *, config: ConfigManager):
        self._config = config
        self._smtp_server = self._config.get("email.smtp")
        self._sender_username = self._config.get("email.username")
        self._sender_name = self._config.get("email.sender_name")
        self._sender_password = self._config.get("email.password")

    def send_email(self, *, subject, html_content, receivers, cc_receivers=None, attachments=None):
        """发送邮件

        :param subject: 邮件主题
        :param receivers: 邮件接收人列表，用','分隔
        :param cc_receivers: 邮件抄送人列表，用','分隔
        :param html_content: HTML格式的邮件内容
        :param attachments: 附件列表，用','分隔
        :return:
        """
        if subject is None or subject == "":
            logging.getLogger(__name__).error("no subject specified")
            return
        if receivers is None or receivers == "":
            logging.getLogger(__name__).error("no receivers specified")
            return
        if html_content is None or html_content == "":
            logging.getLogger(__name__).error("no html_content specified")
            return
        all_receivers = list()
        try:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 添加邮件内容
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            # 添加附件
            if attachments is not None and attachments != "":
                attachment_list = attachments.split(',')
                for attachment in attachment_list:
                    with open(attachment, mode='rb') as f:
                        mime = MIMEText(f.read(), 'base64', 'utf-8')
                        mime['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment)
                        msg.attach(mime)

            # 添加邮件头
            msg['to'] = ",".join(receivers)
            if cc_receivers is not None and cc_receivers != "":
                msg['Cc'] = cc_receivers
            msg['from'] = "{0} <{1}>".format(self._sender_name, self._sender_username)
            msg['subject'] = subject
            server = smtplib.SMTP(self._smtp_server)
            server.starttls()
            server.login(self._sender_username, self._sender_password)
            if cc_receivers is not None and cc_receivers != "":
                all_receivers.extend(cc_receivers.split(','))
            server.sendmail(self._sender_username, receivers, msg.as_string())
            logging.getLogger(__name__).info("mail delivered to %s and cc to %s", receivers, cc_receivers)
            server.close()
        except smtplib.SMTPException as e:
            logging.getLogger(__name__).error("failed to send email to %s, cause: %s", all_receivers, e)
