WITH RECURSIVE search_graph(id, parent, depth, root) AS (
        select pip.id, pip.parent_id, 1, pip.id
        from kb.measurepoint mp
        join kb.measurepointcode mpc
        on mp.code_id = mpc.id
        join kb.pipesegment pip
        on mpc.id = pip.measurepoint_in
        where mp.valid_to > now() AND mp.area_id IS NOT NULL
      UNION ALL
        SELECT pipc.id, pipc.parent_id, search_graph.depth + 1, search_graph.root
        FROM kb.pipesegment pipc, search_graph
        WHERE pipc.parent_id = search_graph.id
)
SELECT *
FROM search_graph
ORDER BY search_graph.root,search_graph.depth