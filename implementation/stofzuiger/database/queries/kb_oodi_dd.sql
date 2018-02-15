WITH RECURSIVE search_graph(id, parent, depth, root, geom, area_id) AS (
  SELECT pip.id, pip.parent_id, 1, pip.id, mp.geom, mp.area_id
  FROM kb.measurepoint mp
  JOIN kb.measurepointcode mpc
  ON mp.code_id = mpc.id
  JOIN kb.pipesegment pip
  ON mpc.id = pip.measurepoint_in
  WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL AND pip.id = %(root_id)s
  UNION ALL
  SELECT pipc.id, pipc.parent_id, search_graph.depth + 1, search_graph.root, search_graph.geom, search_graph.area_id
  FROM kb.pipesegment pipc, search_graph
  WHERE pipc.parent_id = search_graph.id )
SELECT
  area.name as area,
  search_graph.depth as depth,
  mp.id as measurepoint_id,
  EXTRACT(year from rec.date) + (EXTRACT(month from rec.date) / 13) as date_float,
  rec.date,
  mes.value as mep_aan,
  mes2.value as mep_uit,
  mes.value - mes2.value as difference,
  iflens.value as iflens,
  st_distance_sphere(mp.geom,search_graph.geom) as distance
FROM search_graph
  JOIN kb.pipesegment pip
  ON pip.id = search_graph.id
  JOIN kb.measurepointcode mpc
  ON pip.measurepoint_in = mpc.id
  JOIN kb.measurepoint mp
  ON mpc.id = mp.code_id
  JOIN kb.recording rec
  ON mp.id = rec.measurepoint_id
  JOIN kb.area area
  ON search_graph.area_id = area.id
  JOIN kb.measurement mes
  ON rec.id = mes.recording_id AND mes.characteristic_id = 1
  FULL OUTER JOIN kb.measurement mes2
  ON rec.id = mes2.recording_id AND mes2.characteristic_id = 3
  FULL OUTER JOIN kb.measurement iflens
  ON rec.id = iflens.recording_id AND iflens.characteristic_id = 4
WHERE mp.valid_to > now()