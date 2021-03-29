def data_checks(df):
    # check games total
    if not(63 * (END_YEAR - START_YEAR + 1) == df.shape[0]):
        return {"result": "failed", "test": "games total"}
    
    # no ties
    if not(df.loc[df.home_score == df.away_score, ].empty):
        return {"result": "failed", "test": "no ties"}
    
    return {"result": "passed"}