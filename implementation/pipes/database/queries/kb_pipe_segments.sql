WITH RECURSIVE search_graph(id, parent, depth, root, coating) AS (
  SELECT pip.id, pip.parent_id, 1, pip.id, pip.material_type_id
  FROM kb.pipesegment pip
  WHERE pip.id in %(root_ids)s
  UNION ALL
  SELECT pipc.id, pipc.parent_id, search_graph.depth + 1, search_graph.root, pipc.material_type_id
  FROM kb.pipesegment pipc, search_graph
  WHERE pipc.parent_id = search_graph.id AND pipc.measurepoint_in is NULL )

select search_graph.*,
pip.measurepoint_in,
pip.measurepoint_out,
pip.length,
pip.geom,
mp.id as mp_id
from search_graph
join kb.pipesegment pip
on search_graph.id = pip.id
join kb.measurepointcode mpc
on pip.measurepoint_in = mpc.id
join kb.measurepoint mp
on mpc.id = mp.code_id