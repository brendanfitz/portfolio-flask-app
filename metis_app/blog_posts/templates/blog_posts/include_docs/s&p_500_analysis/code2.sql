SELECT
  EXTRACT('year' from s.date),
  AVG(close) AS average_closing_price


FROM visualizations.stock_prices s

GROUP BY 1

ORDER BY 1;
