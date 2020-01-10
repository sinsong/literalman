import re

src_bold      = '(?P<bold>.)\010(?P=bold)'
src_italic    = '_\010([^_])'
src_underline = '_\010.\010(.)'

re_bold      = re.compile(src_bold)
re_italic    = re.compile(src_italic)
re_underline = re.compile(src_underline)

#  group
re_g_bold      = re.compile('(' + src_bold + ')+')
re_g_italic    = re.compile('(' + src_italic + ')+')
re_g_underline = re.compile('(' + src_underline + ')+')

re_manlink = re.compile(r'([^\(\s]+?)\((\S+)\)')
re_url = re.compile(r'(http|https|ftp)://[^\s<>\)]+')
re_sect = re.compile(r'^<b>(.+?)</b>$', flags=re.MULTILINE)

def repl_bold(m):
    return '<b>' + re_bold.sub('\g<1>', m.group(0)) + '</b>'

def repl_italic(m):
    return '<i>' + re_italic.sub('\g<1>', m.group(0)) + '</i>'

def repl_underline(m):
    return '<I>' + re_underline.sub('\g<1>', m.group(0)) + '</I>'

def man_process(s:str):
    s_sped = s.rstrip('\n').split('\n')
    head, content, foot = s_sped[0], '\n'.join(s_sped[1:-1]), s_sped[-1]

    content = content.replace('&', '&amp;')
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    content = re_g_bold.sub(repl_bold, content)
    content = re_g_italic.sub(repl_italic, content)
    content = re_g_underline.sub(repl_underline, content)
    content = re_manlink.sub('<a href="/man?query=\g<1>&section=\g<2>">\g<0></a>', content)
    content = re_url.sub('<a href="\g<0>">\g<0></a>', content)
    content = re_sect.sub('<a href="#\g<1>" id="\g<1>">\g<0></a>', content)
    return '\n'.join([head, content, foot])
