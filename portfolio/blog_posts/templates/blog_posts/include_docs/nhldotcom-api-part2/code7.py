years = [str(x) + str(x+1) for x in range(2000, 2021, 1)]
pagination = [0] + [x * 100 + 1 for x in range(1, 4)]
frames = []

for year in years:
    for start in pagination:
        url = url_base + '?' + generate_qstrobj(qstrobj, start, year)
        response = requests.get(url)
        data = json.loads(response.text)
        frames.append(pd.DataFrame.from_records(data['data']))
