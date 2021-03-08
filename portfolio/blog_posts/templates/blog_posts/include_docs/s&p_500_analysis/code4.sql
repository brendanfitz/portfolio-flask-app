/* 25 Largest Changes in Closing Value */
WITH prices_with_daily_delta AS (
  SELECT
    date,
    LAG(close) OVER (ORDER BY date) AS previous_day_stock_price,
    close,
    close / LAG(close) OVER (ORDER BY date) - 1 AS daily_price_delta

  FROM visualizations.stock_prices
)
SELECT *

FROM prices_with_daily_delta

WHERE date >= '1957-03-04' /* Start of the S&P, there were too many dates in the 1930s without this filter! */

ORDER BY ABS(daily_price_delta) DESC

LIMIT 25;
