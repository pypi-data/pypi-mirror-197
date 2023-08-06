
def send_email(
    to=None,
    cc=None,
    bcc=None,
    subject='',
    body_txt='',
    body_html='',
    email_account='',
    from_description=None,
    email_password='',
    smtp_domain='smtp.gmail.com',
    smtp_port=465
    ):
    '''
    Send an email
    
    to: str or list; specify email addresses for the To line
    
    cc: str or list; specify email addresses for the Cc line
    
    bcc: str or list; specify email addresses for the Bcc line
    
    subject: str; specify the email subject line
    
    body_txt: str; specify the simple text body for the email
        If body_txt is specified and body_html is NOT specified,
         a simple (MIMEText) email will be sent
    
    body_html: str; specify the body for the email, incluing complex
        layout and formatting
        If body_html is specified, a complex (MIMEMultipart) email
        will be sent. A simplified body (body_txt) can ALSO be specified
        and will be encoded along with the complex email body
    
    email_account: str; originating email account
    
    from_description: str or None; text description of the originating email
        account. Example would be 'Notifications'
    
    email_password: str; password for sending email account
    
    smtp_domain: str; smtp domain for sending email account
    
    smtp_port: int; port for smtp domain sending email
    
    '''

    # https://stackoverflow.com/questions/882712/send-html-emails-with-python
    # Text messages through Google Fi via email
    # https://support.google.com/fi/answer/6356597

    addressees = [to, cc, bcc]
    if not any(addressees): 
        raise ValueError('Must include at least one addressee (to, cc, bcc)')
    
    if not any([email_account, email_password]):
        raise ValueError('Must specify sending email account and password (email_account, email_password)')
    
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    for idx in range(len(addressees)):
        if isinstance(addressees[idx], str): addressees[idx] = [addressees[idx]]
        if addressees[idx] is None: addressees[idx] = []
    to, cc, bcc = [list(set(dist)) for dist in addressees]
    all_addressees = list(set([addr for addrs in addressees for addr in addrs]))

    if not from_description: from_description = email_account

    # Simple message for text
    msg_simple = MIMEText(body_txt)

    ## Simple ## 
    # Complex message for email
    msg_alt = MIMEMultipart('alternative')

    ## Complex ##
    # Record the MIME types of both parts - text/plain and text/html.
    plain_part = MIMEText(body_txt, 'plain')
    html_part = MIMEText(body_html, 'html')

    # Prepare both message types
    '''
    To and Cc are included here to SHOW the recipients who the email was
    sent to. Bcc is not included in the message since it would reveal the Bcc
    recipients. The Bcc recipients are still included in the addressees when
    sending the actual message.
    '''

    msg_simple['From'] = from_description
    msg_simple['Subject'] = subject
    msg_simple['To'] = ', '.join(to)
    msg_simple['Cc'] = ', '.join(cc)

    msg_alt['From'] = from_description
    msg_alt['Subject'] = subject
    msg_alt['To'] = ', '.join(to)
    msg_alt['Cc'] = ', '.join(cc)

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg_alt.attach(plain_part)
    msg_alt.attach(html_part)

    smtp_server = smtplib.SMTP_SSL(smtp_domain, smtp_port)
    smtp_server.login(email_account, email_password)
    
    if body_txt and not body_html:
        smtp_server.sendmail(email_account, all_addressees, msg_simple.as_string())
    elif body_html:
        smtp_server.sendmail(email_account, all_addressees, msg_alt.as_string())
    
    smtp_server.quit()
