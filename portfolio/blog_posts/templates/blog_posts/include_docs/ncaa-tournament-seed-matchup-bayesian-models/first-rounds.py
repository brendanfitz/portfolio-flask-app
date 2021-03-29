mask = df.loc[:, 'round'] == 1
first_round_matchups = (df.loc[mask, 'seed_matchup']
    .drop_duplicates()
    .sort_values()
    .tolist()
)


models = dict()

for matchup in first_round_matchups:
    df_matchup = df.loc[df.seed_matchup == matchup, ]
    
    higher_seed, lower_seed = list(map(int, matchup.split('v')))
    
    model = BayesBetaBinomial(matchup, a_prior=lower_seed, b_prior=higher_seed)
    
    x = sum(df_matchup.seed_result == 'higher_seed_win')
    n = df_matchup.shape[0]
    model.update(x, n)
    
    title = f'{higher_seed} vs {lower_seed} Seed Matchups - Bayesian Posterior Distribution'
    ax = model.plot_posterior(title)
    plt.savefig(f'data/{matchup}_posterior_distribution.png')
    plt.show()
    
    models[matchup] = model