pat = r'\d+′ \d+\.?\d?″'
mask = ~ft_inches_str.str.match(pat, na=True)
(df.join(ft_inches_str)
 .loc[mask, ]
 .head()
)
