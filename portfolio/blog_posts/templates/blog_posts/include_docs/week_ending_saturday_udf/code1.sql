CREATE FUNCTION week_ending_saturday(date) RETURNS date AS $$
  SELECT $1 - CASE
                WHEN DATE_PART('dow', $1) = 6
                  THEN 0
                  ELSE (DATE_PART('dow', $1) + 1)::INT
                END
$$ LANGUAGE SQL;
