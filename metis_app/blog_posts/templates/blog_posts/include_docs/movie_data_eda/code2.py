ax = (df.assign(month=lambda x: x.release_date.dt.month)
      .pipe((sns.boxplot, 'data'), x='month', y='domestic_total_gross'))
ax.set_xticklabels(month_names,
                   rotation=45,
                   horizontalalignment='right')
ax.yaxis.set_major_formatter(formatter)
ax.set(title='Domestic Total Gross by Month',
       xlabel='',
       ylabel='')
plt.show()
