ft_inches_str = (df.opponent_height.str.split(' / ', expand=True)[0]
                 .rename('opponent_height_ft_and_inches')
                )
(df.join(ft_inches_str)
 .head()
)
