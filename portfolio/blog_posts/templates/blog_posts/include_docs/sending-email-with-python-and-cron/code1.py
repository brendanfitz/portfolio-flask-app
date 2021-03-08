_rangers = 'New York Rangers'

def scrape_rangers_schedule_df():
    url = 'https://www.hockey-reference.com/teams/NYR/2020_games.html'
    df = pd.read_html(url)[0]

    """ filter out rows that are column header rows within the table """
    mask = df.loc[:, 'GP'] != 'GP'
    df = (df.loc[mask, ]
        .assign(Date=lambda x: pd.to_datetime(x.Date))
        .rename(columns={'Unnamed: 3': 'Home/Away'})
    )
    assert(df.shape[0] == 82)

    return df

def filter_game_data(df, testing=False):
    date_val = dt.datetime(2020, 4, 2) if testing else dt.datetime.today()

    dt_mask = df.Date == date_val
    df_date_filtered = df.loc[dt_mask, ]

    if not df_date_filtered.empty:
        game_data = df_date_filtered.to_dict(orient='record')[0]
        return game_data

def scrape_team_data(opponent):
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_standings.html#all_standings'
    df = (pd.read_html(url, attrs = {'id': 'standings'})[0]
        .rename(columns={'Unnamed: 1': 'Team'})
        .loc[:, ['Team', 'Overall']]
        .set_index('Team')
    )
    teams = [_rangers, opponent]
    team_records = (df.loc[teams, ]
        .to_dict()
        ['Overall']
    )

    return team_records
