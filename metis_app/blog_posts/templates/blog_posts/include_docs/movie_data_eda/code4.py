mask = df.genre.isin(genres)
fig = plt.figure(figsize= [15, 10])
ax = fig.add_subplot(111)
data = df.loc[mask, ['genre', 'roi']]
sns.boxplot(x='genre', y='roi', data=data, showfliers=False)
ax.set_xticklabels(ax.get_xticklabels(),
                   rotation=45,
                   horizontalalignment='right',
                   fontweight='light')
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
ax.set(title='ROI by Genre', xlabel='', ylabel='')
plt.show()
