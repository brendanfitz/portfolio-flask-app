WITH date_filter AS (
  SELECT
    max(week_ending_saturday(date)) - 7 * 4 AS date_start,
    max(week_ending_saturday(date)) AS date_end
  
  FROM visualizations.stock_prices
)
SELECT
  week_ending_saturday(date),
  TO_CHAR(min(close), 'L9,999') AS min_closing_price,
  TO_CHAR(avg(close), 'L9,999') AS average_closing_price,
  TO_CHAR(max(close), 'L9,999') AS max_closing_price,
  COUNT(*) AS trading_days
  
FROM visualizations.stock_prices

LEFT JOIN date_filter
       ON 1 = 1

WHERE date between date_start and date_end

GROUP BY 1

ORDER BY 1;
