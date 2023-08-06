
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

## string_tools
Tools and utilities related to manipulating strings

### to_preheader_text_html
Create an HTML string for use in an email body to customize the email preview text when viewing an email in an inbox. Ref this [preview text article](https://www.litmus.com/blog/the-little-known-preview-text-hack-you-may-want-to-use-in-every-email/).
    
- `preheader_text`: str; string (including unicode or emoji) to be added to the HTML
- `tag_type`: str; 'span' (default) or 'div'. Adapted from a [MailChimp method](https://stackoverflow.com/questions/45807788/preheader-text-in-html-email/51218077#51218077)
- `target_text_len`: int; length of text to fill
    - Some email previews will fill in body text to the preview if the preheader text does not completely fill the space
- `space_filler`: str; characters to fill difference between actual preheader text and the target_text_len.

Review the [`send_email`](email_tools.md#send_email) documentation for more detail.

```py
from hotbrush.string_tools import to_preheader_text_html

preheader_text = 'Oh man you really have to read this'

preheader = to_preheader_text_html(preheader_text)

# Send an email
from hotbrush.email_tools import send_email
...

body_html = f'{preheader}<h1><b>OTHER THINGS</b></h1>'
...
# See the email_tools#send_email documentation for more detail

```

### to_styled_unicode
Replace normal ASCII characters with styled Unicode characters. Direct use-case is for email sender and subject line modification. If no transformed character is found, the original character is returned.

- `characters`: str or list; convert plain text (letters, sometimes numbers, sometimes punctuation) to obscure characters from Unicode. Direct use-case is for replacing characters. Directly from [Unicode Text Converter](https://qaz.wtf/u/convert.cgi)
- `transform`: str; name of Unicode transform to convert characters to 'print' to display the name and available characters for each transform

```py
from hotbrush.string_tools import to_styled_unicode

custom_subject = to_styled_unicode('🤔🤔 Hey HEY', 'math bold italic')
custom_subject += ', '
custom_subject += to_styled_unicode('check out my sweet ', 'math bold')
custom_subject += to_styled_unicode('subject line')

print(custom_subject)
🤔🤔 𝑯𝒆𝒚 𝑯𝑬𝒀, 𝐜𝐡𝐞𝐜𝐤 𝐨𝐮𝐭 𝐦𝐲 𝐬𝐰𝐞𝐞𝐭 🆂🆄🅱🅹🅴🅲🆃 🅻🅸🅽🅴
```
