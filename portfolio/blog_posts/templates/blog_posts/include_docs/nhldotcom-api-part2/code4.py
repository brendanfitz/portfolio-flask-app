import urllib.parse as up

url_base, qstr = url.split('?')
up.parse_qs(qstr)
