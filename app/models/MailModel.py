from flask import render_template
from flask_mail import Message

from app import mail
# from app.resources.UsersResource import get_admin_mail
from app.resources.MerchResource import get_item_from_merch


class Mail:
    def __init__(self, topic, content, settings, reply_email='info@czzk.pl', recipients='info@czzk.pl'):
        """
        Mail attributes:
        :param topic:
        :param content: String or sign up form.
        :param recipients:
        :param reply_email:
        :param mail_type: Basic (default) email with no template (None), confirm email or notification email.
        """

        # Check for admin mail
        # admin_mail = get_admin_mail()
        # if admin_mail:
        #     recipients = admin_mail

        recipients = 'psambek@gmail.com'

        self.settings = settings
        self.topic = self.build_topic(topic)
        self.raw_topic = topic
        self.reply_email = reply_email
        self.content = self.build_content(self.reformat_message(content))
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
