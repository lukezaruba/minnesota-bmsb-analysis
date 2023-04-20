# Raster Extraction Script
# Luke Zaruba
# April 18, 2023

# Run from main project directory

# Set URLs
$LandcoverURL = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/biota_landcover_nlcd_mn_2019/tif_biota_landcover_nlcd_mn_2019.zip"
$ElevationURL = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/elev_30m_digital_elevation_model/fgdb_elev_30m_digital_elevation_model.zip"
$CitiesURL = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dot/bdry_mn_city_township_unorg/shp_bdry_mn_city_township_unorg.zip"

# Set up Dir Paths
$wd = pwd
$DataDir = Join-Path -Path $wd -ChildPath "data"
$LcDir = Join-Path -Path $DataDir -ChildPath "landcover"
$ElevDir = Join-Path -Path $DataDir -ChildPath "elevation"
$CityDir = Join-Path -Path $DataDir -ChildPath "cities"

$LandcoverZip = Join-Path -Path $LcDir -ChildPath "landcover.zip"
$ElevationZip = Join-Path -Path $ElevDir -ChildPath "elevation.zip"
$CitiesZip = Join-Path -Path $CityDir -ChildPath "cities.zip"

# Create Dirs
New-Item -Path $LcDir -ItemType Directory
New-Item -Path $ElevDir -ItemType Directory
New-Item -Path $CityDir -ItemType Directory

# Landcover
Write-Host "Downloading 2019 NLCD Landcover Raster for Minnesota..."
Invoke-WebRequest -Uri $LandcoverURL -OutFile $LandcoverZip
Write-Host "Unzipping 2019 NLCD Landcover Raster for Minnesota..."
Expand-Archive $LandcoverZip -DestinationPath $LcDir -Force

# Elevation
Write-Host "Downloading Elevation Raster for Minnesota..."
Invoke-WebRequest -Uri $ElevationURL -OutFile $ElevationZip
Write-Host "Unzipping 2019 NLCD Landcover Raster for Minnesota..."
Expand-Archive $ElevationZip -DestinationPath $ElevDir -Force

# Cities
Write-Host "Downloading Cities Dataset for Minnesota..."
Invoke-WebRequest -Uri $CitiesURL -OutFile $CitiesZip
Write-Host "Unzipping Cities Dataset for Minnesota..."
Expand-Archive $CitiesZip -DestinationPath $CityDir -Force
