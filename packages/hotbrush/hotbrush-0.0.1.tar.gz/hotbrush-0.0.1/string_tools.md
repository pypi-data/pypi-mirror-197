
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