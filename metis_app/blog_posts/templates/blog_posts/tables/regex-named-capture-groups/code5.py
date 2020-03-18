pat = r'(?P<feet>\d+)′ (?P<inches>\d+\.?\d?)″'
ft_inch_columns = ft_inches_str.str.extract(pat).astype('float64')
(df.join(ft_inch_columns)
 .head()
 .to_html(**html_kwargs)
)
