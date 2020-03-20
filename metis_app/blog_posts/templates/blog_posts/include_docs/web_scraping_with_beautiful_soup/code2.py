url = 'https://www.boxofficemojo.com/title/tt2293640/'
title = 'Minions'
field_dict = {
    'release_date': 'Release Date:',
    'distributor': 'Distributor',
    'rating': 'MPAA Rating',
    'genre': 'Genre: ',
    'runtime': 'Runtime:',
    'budget': 'Production Budget:',
    'domestic_total_gross': 'Domestic Total Gross'
}
movie_scrape(title, url, field_dict)
