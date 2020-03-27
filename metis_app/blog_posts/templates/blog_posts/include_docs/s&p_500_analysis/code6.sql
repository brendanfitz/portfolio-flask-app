/* Max Intra-Day Trading Range */
SELECT
  date,
  open,
  low,
  high,
  (high - low) / open  as intraday_trading_range_over_opening

FROM visualizations.stock_prices

ORDER BY 5 DESC

LIMIT 25;
