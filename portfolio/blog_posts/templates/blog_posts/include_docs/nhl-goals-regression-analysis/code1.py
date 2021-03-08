def create_lags(input_df, metric, n=5, include_metric_name_in_columns=False):
    df = input_df.copy()
    frames = [df.groupby('skaterFullName')[metric].shift(i) for i in range(n+1)]
    if include_metric_name_in_columns:
        keys = [metric] + [metric + '_L%s' % i for i in range(1, n+1)]
    else:
        keys = ['y'] + ['L%s' % i for i in range(1, n+1)]
    df = (pd.concat(frames, axis=1, keys=keys)
        .dropna()
    )
    return df
