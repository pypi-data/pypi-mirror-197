
# Directly from Unicode Text Converter at https://qaz.wtf/u/convert.cgi
styled_unicode_map = {
    'original': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz'),
    'circled': list('`①②③④⑤⑥⑦⑧⑨0⊖⊜~!@#$%^&⊛()⊖⊜,⨀⊘⧀⧁?;\':"[]{}⦸⦶ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'),
    'circled neg': list('`123456789⓿-=~!@#$%^&*()-=,./<>?;\':"[]{}\|🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩 🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩'),
    'fullwidth': list('｀１２３４５６７８９０－＝～！＠＃＄％＾＆＊（）－＝，．／<>？；＇："［］｛｝＼｜ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'),
    'math bold': list('`𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙 𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳'),
    'math bold fraktur': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅 𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟'),
    'math bold italic': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁 𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛'),
    'math bold script': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩 𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃'),
    'math double-struck': list('`𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ 𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫'),
    'math monospace': list('`𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉 𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣'),
    'math sans': list('`𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹 𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓'),
    'math sans bold': list('`𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭 𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇'),
    'math sans bold italic': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕 𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯'),
    'math sans italic': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡 𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻'),
    'parenthesized': list('`⑴⑵⑶⑷⑸⑹⑺⑻⑼0-=~!@#$%^&*()-=,./<>?;\':"[]{}\|⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵ ⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵'),
    'regional indicator': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿 🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿'),
    'squared': list('`1234567890⊟=~!@#$%^&⧆()⊟=,⊡⧄<>?;\':"[]{}⧅|🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉 🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉'),
    'squared neg': list('`1234567890-=~!@#$%^&*()-=,./<>?;\':"[]{}\|🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉 🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉'),
}

def to_preheader_text_html(
    preheader_text='🤔 How is he doing that?',
    tag_type='span',
    target_text_len=120,
    space_filler='&#847;&zwnj;&nbsp;'
    ):
    '''
    Create an HTML string for use in an email body to customize the email preview 
        text when viewing an email in an inbox
    
    preheader_text: str; string (including unicode or emoji) to be added to the HTML
    
    tag_type: str; 'span' (default) or 'div'. Adapted from a MailChimp method
        https://stackoverflow.com/questions/45807788/preheader-text-in-html-email/51218077#51218077
    
    target_text_len: int; length of text to fill
        Some email previews will fill in body text to the preview if the preheader text 
        does not completely fill the space
        Reference article: https://www.litmus.com/blog/the-little-known-preview-text-hack-you-may-want-to-use-in-every-email/
    
    space_filler: str; characters to fill difference between actual preheader text and
        the target_text_len.
    
    '''

    if len(preheader_text) < target_text_len:
        preheader_text += (target_text_len - len(preheader_text)) * space_filler

    preheader_text_html = (
    f'''
    <{tag_type} style="
        display:none;
        font-size:0px;
        line-height:0px;
        max-height:0px;
        max-width:0px;
        opacity:0;
        overflow:hidden;
        visibility:hidden;
        mso-hide:all;
    ">{preheader_text}</{tag_type}>
    '''
    )
    
    return preheader_text_html


def to_styled_unicode(characters='', transform='squared neg'):
    '''
    Replace normal ASCII characters with styled Unicode characters. Direct use-case is for email sender and
        subject line modification. If no transformed character is found, the original character is returned.
    
    characters: str or list; convert plain text (letters, sometimes numbers, sometimes punctuation)
        to obscure characters from Unicode. Direct use-case is for replacing characters
        Directly from Unicode Text Converter at https://qaz.wtf/u/convert.cgi
    
    transform: str; name of Unicode transform to convert characters to
        'print' to display the name and available characters for each transform
        
    Returns a string of converted characters
    '''
    
    if transform.lower() == 'print': 
        for k, v in styled_unicode_map.items():
            print(f"'{k}': {''.join(v)}")
        return
        
    if not isinstance(characters, list): characters = list(characters)
    return_characters = []
    for character in characters:
        if character not in styled_unicode_map['original']:
            return_characters.append(character)
        else:
            return_characters.append(styled_unicode_map[transform][styled_unicode_map['original'].index(character)])
    return ''.join(return_characters)
