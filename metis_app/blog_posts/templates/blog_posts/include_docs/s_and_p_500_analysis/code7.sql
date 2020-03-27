/* 200-day close moving-average crossings */
WITH prices_with_ma AS (
  SELECT
    date,
    close,
    AVG(close) OVER (ORDER BY date ROWS BETWEEN 200 - 1 PRECEDING AND CURRENT ROW) AS close_200d_ma

  FROM visualizations.stock_prices

  WHERE date >= '1957-03-04' /* Start of the S&P, there were too many dates in the 1930s without this filter! */
),
prices_with_ma_lagged AS (
SELECT
  *,
  close - close_200d_ma AS close_minus_200d_ma,
  LAG(close - close_200d_ma) OVER (ORDER BY date) AS close_minus_200d_ma_lagged


FROM prices_with_ma
)
SELECT *

FROM prices_with_ma_lagged

WHERE (close_minus_200d_ma > 0 and close_minus_200d_ma_lagged < 0)
   OR (close_minus_200d_ma < 0 and close_minus_200d_ma_lagged > 0)
   OR close_minus_200d_ma = 0;
