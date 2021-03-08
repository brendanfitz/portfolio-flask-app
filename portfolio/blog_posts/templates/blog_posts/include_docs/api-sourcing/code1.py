import pandas as pd

def mta_data(week_numbers):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
    frames = list()
    for week_number in week_numbers:
        file_url = url.format(week_number)
        df = pd.read_csv(file_url)
        frames.append(df)
    return pd.concat(frames)
