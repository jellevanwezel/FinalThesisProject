WITH RECURSIVE rec_tree(id, parent, depth, root, root_geom) AS (
        SELECT pip.id, pip.parent_id, 1, pip.id, mp.geom
        FROM kb.measurepoint mp
        JOIN kb.measurepointcode mpc
        ON mp.code_id = mpc.id
        JOIN kb.pipesegment pip
        ON mpc.id = pip.measurepoint_in
        WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL
      UNION ALL
        SELECT pipc.id, pipc.parent_id, rec_tree.depth + 1, rec_tree.root, rec_tree.root_geom
        FROM kb.pipesegment pipc, rec_tree
        WHERE pipc.parent_id = rec_tree.id
)
SELECT rec_tree.*,
pip.construction_year,
pip.material_type_id,
pip.geom as pipe_geom,
mp.geom as mp_geom,
rec.date as rec_date,
mes.value as mes_val,
ST_DistanceSphere(mp.geom,rec_tree.root_geom) as dist_to_root,
st_x(mp.geom) as mx,st_y(mp.geom) as my,
st_x(rec_tree.root_geom) as rx, st_y(rec_tree.root_geom) as ry
FROM rec_tree
JOIN kb.pipesegment pip
ON pip.id = rec_tree.id
FULL OUTER JOIN kb.measurepointcode mpc
ON pip.measurepoint_in = mpc.id
FULL OUTER JOIN kb.measurepoint mp
ON mpc.id = mp.code_id
FULL OUTER JOIN kb.recording rec
ON mp.id = rec.measurepoint_id
FULL OUTER JOIN kb.measurement mes
ON rec.id = mes.recording_id
WHERE (mp.valid_to > now() OR mp.valid_to IS NULL) AND (mes.characteristic_id = 3 OR mes.characteristic_id IS NULL)
ORDER BY rec_tree.root,rec_tree.depth
