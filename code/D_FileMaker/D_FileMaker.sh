#! /bin/bash

base_dir=$(cd "$(dirname "$0")";pwd)

if [ ! -d "$base_dir/download/" ]; then
	echo "folder:$base_dir/download/ is not exist!"
	exit 0
fi

if [ ! -f "$base_dir/FileMaker.py" ]; then
	echo "file:$base_dir/FileMaker.py is not exist!"
	exit 0
fi

ls_date=`date +%Y%m%d`
echo "$ls_date"

echo "tar&zip->$base_dir/$ls_date.tar.gz"
tar -czf $ls_date.tar.gz download/

python3 $base_dir/FileMaker.py 3205 $ls_date.tar.gz udisk-down_zip.sh