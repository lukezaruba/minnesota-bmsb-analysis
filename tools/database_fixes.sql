-- Create New Copies of Databases
CREATE TABLE final_huff AS TABLE huff_model;
CREATE TABLE final_huff_decay AS TABLE huff_model_distance_decay;
CREATE TABLE final_gravity AS TABLE gravity_model;

-- Fix CRS
ALTER TABLE final_huff
	ALTER COLUMN geom
	TYPE Geometry(Point, 4326) 
	USING ST_Transform(ST_SetSRID(geom, 26915), 4326);

ALTER TABLE final_huff_decay
	ALTER COLUMN geom
	TYPE Geometry(Point, 4326) 
	USING ST_Transform(ST_SetSRID(geom, 26915), 4326);

ALTER TABLE final_gravity
	ALTER COLUMN geom
	TYPE Geometry(Point, 4326) 
	USING ST_Transform(ST_SetSRID(geom, 26915), 4326);

-- Drop Duplicates
ALTER TABLE final_huff ADD id SERIAL;
DELETE FROM
    final_huff x
        USING final_huff y
WHERE
    x.id < y.id
    AND x.city = y.city;

ALTER TABLE final_huff_decay ADD id SERIAL;
DELETE FROM
    final_huff_decay x
        USING final_huff_decay y
WHERE
    x.id < y.id
    AND x.city = y.city;

ALTER TABLE final_gravity ADD id SERIAL;
DELETE FROM
    final_gravity x
        USING final_gravity y
WHERE
    x.id < y.id
    AND x.city = y.city;
