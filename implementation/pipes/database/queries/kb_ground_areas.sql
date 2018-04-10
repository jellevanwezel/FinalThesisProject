SELECT
  t.id as id,
  t.ph as acid,
  t.gw_class as ground_water,
  t.stability as stability,
  t.type as ground_type,
  t.geom as geom
  FROM kb.soil t
  ORDER BY id