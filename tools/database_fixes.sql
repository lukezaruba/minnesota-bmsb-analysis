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
