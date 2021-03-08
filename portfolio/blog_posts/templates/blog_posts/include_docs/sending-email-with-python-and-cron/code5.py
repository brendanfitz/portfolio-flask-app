opponent = game_data['Opponent']

team_records = scrape_team_data(opponent)

template_kwargs = dict(
    opponent=opponent,
    time=game_data['Time'],
    rangers_record=team_records[_rangers],
    opponent_record=team_records[opponent],
)
text = text_template.render(**template_kwargs)
html = html_template.render(**template_kwargs)
