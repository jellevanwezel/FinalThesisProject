WITH RECURSIVE search_graph(id, parent, root, area_id) AS (
  SELECT pip.id, pip.parent_id, pip.id, mp.area_id
  FROM kb.measurepoint mp
  JOIN kb.measurepointcode mpc
  ON mp.code_id = mpc.id
  JOIN kb.pipesegment pip
  ON mpc.id = pip.measurepoint_in
  WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL
  UNION ALL
  SELECT pipc.id, pipc.parent_id, search_graph.root, search_graph.area_id
  FROM kb.pipesegment pipc, search_graph
  WHERE pipc.parent_id = search_graph.id )
SELECT
  area.name as area,
  area.id as area_id,
  pip.id as pip_id,
  mp.id as measurepoint_id
FROM search_graph
  JOIN kb.pipesegment pip
  ON pip.id = search_graph.id
  JOIN kb.measurepointcode mpc
  ON pip.measurepoint_in = mpc.id
  JOIN kb.measurepoint mp
  ON mpc.id = mp.code_id
  JOIN kb.area area
  ON search_graph.area_id = area.id
WHERE mp.valid_to > now()