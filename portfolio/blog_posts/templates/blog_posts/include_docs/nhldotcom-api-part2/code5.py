def urlencode_wrapper(qstrobj):
    return (up.urlencode(qstrobj, quote_via=up.quote)
        .replace('%3D', '=')
        .replace('%3A', ':')
        .replace('%2C', ',')
        .replace('%5B%27', '')
        .replace('%27%5D', '')
    )

assert(qstr == urlencode_wrapper(up.parse_qs(qstr)))
