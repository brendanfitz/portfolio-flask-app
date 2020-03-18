pat = r'(?P&lt;feet&gt;\d+)′ (?P&lt;inches&gt;\d+\.?\d?)″'
ft_inch_columns = ft_inches_str.str.extract(pat).astype('float64')
(df.join(ft_inch_columns)
 .head()
 .to_html(**html_kwargs)
)
