SELECT pip.id as id, area.name as area_name
FROM kb.measurepoint mp
JOIN kb.measurepointcode mpc
ON mp.code_id = mpc.id
JOIN kb.pipesegment pip
ON mpc.id = pip.measurepoint_in
JOIN kb.area area
ON mp.area_id = area.id
WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL