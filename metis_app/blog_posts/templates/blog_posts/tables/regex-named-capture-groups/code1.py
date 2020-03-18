import pandas as pd

html_kwargs = dict(
    classes="table",
    justify="left",
    border=0,
    index_names=False
)

fin = r'data\FuryWilderFightHistory.xlsx'
df = (pd.read_excel(fin)
      .loc[:, ['name', 'opponent_name', 'opponent_height',]]
      .drop_duplicates()
      .set_index(['name', 'opponent_name',])
     )
df.head()
