SELECT
  EXTRACT('year' from s.date) as trading_year,
  AVG(close) AS average_closing_price


FROM visualizations.stock_prices s

GROUP BY 1

ORDER BY 1;
