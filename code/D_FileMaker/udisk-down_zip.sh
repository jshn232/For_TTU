rm /app/download.tar.gz
rm -fr /app/download
mv /app/main_1.bin /app/download.tar.gz
tar -xzvf /app/download.tar.gz -C /app/
chmod 777 /app/download/setup.sh
/app/download/setup.sh
