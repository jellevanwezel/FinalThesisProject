WITH RECURSIVE search_graph(id, parent, depth, root, root_geom) AS (
  SELECT pip.id, pip.parent_id, 1, pip.id, mp.geom
  FROM kb.measurepoint mp
  JOIN kb.measurepointcode mpc
  ON mp.code_id = mpc.id
  JOIN kb.pipesegment pip
  ON mpc.id = pip.measurepoint_in
  WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL AND pip.id = %(root_id)s
  UNION ALL
  SELECT pipc.id, pipc.parent_id, search_graph.depth + 1, search_graph.root, search_graph.root_geom
  FROM kb.pipesegment pipc, search_graph
  WHERE pipc.parent_id = search_graph.id )
SELECT
  st_distance_sphere(mp.geom,search_graph.root_geom) as distance,
  mes.value
FROM search_graph
  JOIN kb.pipesegment pip
  ON pip.id = search_graph.id
  JOIN kb.measurepointcode mpc
  ON pip.measurepoint_in = mpc.id
  JOIN kb.measurepoint mp
  ON mpc.id = mp.code_id
  JOIN kb.recording rec
  ON mp.id = rec.measurepoint_id
  JOIN kb.measurement mes
  ON rec.id = mes.recording_id
WHERE mp.valid_to > now() AND (mes.characteristic_id = 1)