ft_inches_str = (df.opponent_height.str.split(' / ', expand=True)[0]
                 .str.strip()
                 .str.replace('½', '.5')
                )
pat = r'\d+′ \d+\.?\d?″'
mask = ~ft_inches_str.str.match(pat, na=True)
(df.join(ft_inches_str)
 .loc[mask, ]
 .head()
)
