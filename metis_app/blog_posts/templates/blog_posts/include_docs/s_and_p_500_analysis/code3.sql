/* Max Cloing Price with Date Per Year */
WITH prices_with_max_close_date AS (
  SELECT
    EXTRACT('year' from date) AS trading_year,
    date,
    close,
    first_value(date) over (PARTITION BY EXTRACT('year' from date) ORDER BY EXTRACT('year' from date), close DESC) AS max_close_date
  FROM visualizations.stock_prices
)
SELECT
  trading_year,
  date,
  close as max_closing_value

FROM prices_with_max_close_date

WHERE date = max_close_date

ORDER BY 1;
