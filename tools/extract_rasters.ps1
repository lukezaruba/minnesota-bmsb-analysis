# Raster Extraction Script
# Luke Zaruba
# April 18, 2023

# Set Vars
$LandcoverURL = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/biota_landcover_nlcd_mn_2019/tif_biota_landcover_nlcd_mn_2019.zip"
$ElevationURL = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/elev_30m_digital_elevation_model/fgdb_elev_30m_digital_elevation_model.zip"

$wd = pwd
$outDir = Join-Path -Path $wd -ChildPath "data"
$LandcoverZip = Join-Path -Path $outDir -ChildPath "landcover.zip"
$ElevationZip = Join-Path -Path $outDir -ChildPath "elevation.zip"


# Landcover
Write-Host "Downloading 2019 NLCD Landcover Raster for Minnesota..."
Invoke-WebRequest -Uri $LandcoverURL -OutFile $LandcoverZip
Write-Host "Unzipping 2019 NLCD Landcover Raster for Minnesota..."
Expand-Archive $LandcoverZip -DestinationPath $outDir -Force

# Elevation
Write-Host "Downloading Elevation Raster for Minnesota..."
Invoke-WebRequest -Uri $ElevationURL -OutFile $ElevationZip
Write-Host "Unzipping 2019 NLCD Landcover Raster for Minnesota..."
Expand-Archive $ElevationZip -DestinationPath $outDir -Force
