ax = sns.boxplot(x='rating', y='roi', data=df, order=rating_order, showfliers=False)
ax.set(title='ROI by Rating', xlabel='', ylabel='')
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
plt.show()
