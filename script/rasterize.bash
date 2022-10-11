#!/bin/bash

if [[ $# -ne 3 ]]; then
	echo "usage : bash rasterize.bash FILE.csv outputDirectory epsgCode"
	exit 1
fi

dataSource=$1
FILENAME=$(basename "$1")
outputPath=$2
epsgCode=$3

mkdir -p $outputPath

echo "input filename = " $FILENAME
VRT="${FILENAME%.*}.vrt"
echo "create virtual file format = " $VRT


echo "<OGRVRTDataSource>
    <OGRVRTLayer name=\"${FILENAME%.*}\">
        <SrcDataSource>$dataSource</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <GeometryField encoding=\"PointFromColumns\" x=\"field_1\" y=\"field_2\" z=\"field_3\"/>
    </OGRVRTLayer>
</OGRVRTDataSource>" > $VRT



interpolations=("invdist" "average" "nearest" "linear")
#powers=("1.1" "1.2" "1.4" "1.6" "1.8" "2" "2.2" "2.4" "2.6" "2.8" "3")
#smoothings=("1" "1.5" "2" "2.5" "3" "4" "5" "10")
powers=("1.1" "2.0")
smoothings=("1.0" "2.0")
for interpolationAlgo in ${interpolations[@]}; do
	if [[ "$interpolationAlgo" == "invdist" ]]; then
		# default parameter
		layerName="${FILENAME%.*}"
		rasterName="${layername}_${interpolationAlgo}.tiff"
		gdal_grid -zfield "field_3" -a_srs EPSG:$epsgCode -a $interpolationAlgo -ot Float64 -l $layerName $VRT $outputPath/$rasterName --config GDAL_NUM_THREADS ALL_CPUS
		for power in ${powers[@]}; do
			# echo $power
			for smoothing in ${smoothings[@]}; do
				# custom parameter
				layerName="${FILENAME%.*}"
				rasterName="${layername}_${interpolationAlgo}_p${power}_s${smoothing}.tiff"
				gdal_grid -zfield "field_3" -a_srs EPSG:$epsgCode -a $interpolationAlgo:power=$power:smoothing=$smoothing -ot Float64 -l $layerName $VRT $outputPath/$rasterName --config GDAL_NUM_THREADS ALL_CPUS
			done
		done
	else
		layerName="${FILENAME%.*}"
		rasterName="${layername}_${interpolationAlgo}.tiff"
		gdal_grid -zfield "field_3" -a_srs EPSG:$epsgCode -a $interpolationAlgo -ot Float64 -l $layerName $VRT $outputPath/$rasterName --config GDAL_NUM_THREADS ALL_CPUS
	fi
done
