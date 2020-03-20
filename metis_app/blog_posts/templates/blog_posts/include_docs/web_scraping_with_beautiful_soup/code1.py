import re
import request
import BeautifulSoup

def movie_scrape(title, url, field_dict):
    response = requests.get(base_url + url)
    if response.status_code != 200:
        print("HTTP Error %s: %s" (response.code, response.url))
        return None
    soup = BeautifulSoup(response.text, 'html5lib')
    record = dict()
    record['title'] = title
    record['url'] = url
    for col, field_name in field_dict.items():
        record[col] = movie_val(soup, field_name)
    record['director'] = table_list(soup, 'Director')
    record['actors'] = table_list(soup, 'Actors')

    rows = table_rows(soup, re.compile('Domestic.*Summary'))
    record['open_wkend_gross'] = table_val(rows, 'Opening.*Weekend')
    record['widest_release'] = (table_val(rows, 'Widest.*Release')
                             .replace(' theaters', ''))
    record['in_release'] = table_val(rows, 'In.*Release')
    return record

def movie_val(soup, field_name):
    """Grab a value from boxofficemojo HTML
    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    """
    obj = soup.find(text=re.compile(field_name))
    if obj:
        next_sibling = obj.findNextSibling()
        if next_sibling:
            return next_sibling.text
    return None
