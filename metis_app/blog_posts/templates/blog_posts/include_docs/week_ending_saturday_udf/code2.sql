SELECT
  date,
  week_ending_saturday(date),
  to_char(date, 'Day') as weekday

FROM visualizations.stock_prices

ORDER BY date DESC

LIMIT 15;
