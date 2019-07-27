from flask import render_template
from flask_mail import Message

from app import mail
# from app.resources.UsersResource import get_admin_mail
from app.resources.MerchResource import get_item_from_merch


class Mail:
    def __init__(self, topic, content, settings, reply_email='info@czzk.pl', recipients='info@czzk.pl', raw_mail=False):
        """
        Mail attributes:
        :param topic:
        :param content:
        :param recipients:
        :param reply_email:
        :param settings:
        """

        # Check for admin mail
        # admin_mail = get_admin_mail()
        # if admin_mail:
        #     recipients = admin_mail

        self.raw_mail = raw_mail
        self.settings = settings
        self.topic = self.build_topic(topic) if not raw_mail else topic
        self.raw_topic = topic
        self.reply_email = reply_email
        self.content = self.build_content(self.reformat_message(content)) if not raw_mail else content
        self.recipients = [recipients]

    @staticmethod
    def reformat_message(content):
        """
        Replaces new line signs to html types.

        :return: New content.
        """
        return content.replace('\r\n', "<br>")

    def build_topic(self, topic):
        """
        Build topic content basing on contact form type.
        :return Topic string:
        """

        form_type = self.settings.get('type')

        if form_type == 'merch':
            item_short = self.settings.get('item')

            # Get humanized product name
            merch_item_name = get_item_from_merch(item_short).name

            return '[czzk.pl - merch] ' + merch_item_name

        else:
            return '[czzk.pl - formularz] "' + topic + '"'

    def build_content(self, content):
        """
        Build message content basing on contact form type.
        :return Message html:
        """

        mail_data = {
            'topic': self.raw_topic,
            'sender': self.reply_email,
            'content': content
        }

        form_type = self.settings.get('type')

        if form_type == 'merch':
            item_short = self.settings.get('item')

            # Get humanized product name
            merch_item_name = get_item_from_merch(item_short).name

            return render_template('email.html', type=form_type, item=merch_item_name, mail_data=mail_data)

        return render_template('email.html', type=form_type, item=None, mail_data=mail_data)

    def send(self):
        """
        Sends a message.
        """
        msg = Message(self.topic,
                      recipients=self.recipients,
                      html=self.content,
                      reply_to=self.reply_email)
        mail.send(msg)
