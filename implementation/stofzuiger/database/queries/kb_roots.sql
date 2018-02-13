SELECT pip.id
FROM kb.measurepoint mp
JOIN kb.measurepointcode mpc
ON mp.code_id = mpc.id
JOIN kb.pipesegment pip
ON mpc.id = pip.measurepoint_in
WHERE mp.valid_to > now() AND mp.area_id IS NOT NULL