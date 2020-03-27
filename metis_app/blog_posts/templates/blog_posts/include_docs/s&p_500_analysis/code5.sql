/* Average Deviation by Decade */
WITH prices_with_daily_delta AS (
  SELECT
    date,
    LAG(close) OVER (ORDER BY date) AS previous_day_stock_price,
    close,
    close / LAG(close) OVER (ORDER BY date) - 1 AS daily_price_delta

  FROM visualizations.stock_prices
)
SELECT
  EXTRACT('decade' FROM date) AS trading_year,
  AVG(daily_price_delta) * 100 AS average_daily_deviation

FROM prices_with_daily_delta

GROUP BY 1

ORDER BY 1;
