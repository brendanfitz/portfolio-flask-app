df = scrape_rangers_schedule_df()
game_data = filter_game_data(df, testing=testing)
if game_data is None:
    return
