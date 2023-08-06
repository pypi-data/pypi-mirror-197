
## email_tools
Tools and utilities related to email

### send_email
Send an email.

- `to`: str or list; specify email addresses for the To line
- `cc`: str or list; specify email addresses for the Cc line
- `bcc`: str or list; specify email addresses for the Bcc line
- `subject`: str; specify the email subject line. Can be altered with [string_tools](string_tools.md)
- `body_txt`: str; specify the simple text body for the email
    - If body_txt is specified and `body_html` is NOT specified, a simple (MIMEText) email will be sent
- `body_html`: str; specify the body for the email, incluing complex layout and formatting
    - If body_html is specified, a complex (MIMEMultipart) email will be sent. A simplified body (`body_txt`) can ALSO be specified and will be encoded along with the complex email body
- `email_account`: str; originating email account
- `from_description`: str or None; text description of the originating email account. Example would be 'Notifications'. Can be altered with [string_tools](string_tools.md)
- `email_password`: str; password for sending email account
- `smtp_domain`: str; smtp domain for sending email account
- `smtp_port`: int; port for smtp domain sending email

```py
from hotbrush.email_tools import send_email

# Simple text
body_txt = f"Head's up, your {device} battery is at {pct}!!"
# HTML body
body_html = "<h1>Head's up, your {device} battery is at <b>{pct}</b>!!</h1>"

send_email(
    email_account='sendaccount@gmail.com',
    from_description='Automated alerts',
    email_password='abc123jkjk',
    
    to='my_account@gmail.com',
    subject=f'Your {device} battery is at {pct}',
    body_txt=body_txt,
    body_html=body_html,
)


# Make it a little more fun with `string_tools`
from hotbrush.string_tools import to_preheader_text_html, to_styled_unicode

# Custom 'preview' text, different from message body
preheader = to_preheader_text_html('One simple trick for understanding devices')

# Change from_description and subject line 'font' by altering characters used
from_description = to_styled_unicode('Automated alerts', 'math bold script')
subject = '⚠️🚨🥵 ' + to_styled_unicode(f'Your {device} battery is at {pct}')

send_email(
    email_account='sendaccount@gmail.com',
    from_description=from_description,
    email_password='abc123jkjk',
    
    to='my_account@gmail.com',
    subject=subject,
    body_txt=body_txt,
    body_html=body_html,
)


```