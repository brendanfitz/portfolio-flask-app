qstrobj = up.parse_qs(qstr)
qstrobj['cayenneExp'][0] = qstrobj['cayenneExp'][0].replace('20192020', '{year}')

def generate_qstrobj(qstrobj, start, year):
    qstrobj = copy.deepcopy(qstrobj)
    qstrobj['start'] = start
    qstrobj['cayenneExp'][0] = qstrobj['cayenneExp'][0].format(year=year)
    return urlencode_wrapper(qstrobj)
