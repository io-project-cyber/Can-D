#!/bin/bash

#Use this on a computer running MySQL server to create a table of the specified name in the specified database. Imports csv-storage/toImport.csv 
while getopts d:t:h: flag
do
    case "${flag}" in
        d) database_name=${OPTARG};;
        t) table_name=${OPTARG};;
    esac
done

cd ..

if [ ! -f ./csv-storage/toImport.csv ];
    #If csv-storage/toImposrt.csv doesn't exist, THIS COMMAND IS RAN.
    ./can-d.py -v -pO -o ./csv-storage/toImport.csv
fi
toImportFilePath="'"
toImportFilePath+=$(pwd)
toImportFilePath+="/csv-storage/toImport.csv'"

echo "CREATE DATABASE $database_name;" > sql-server-commands.txt
echo "SET GLOBAL local_infile=1;" >> sql-server-commands.txt
sudo mysql < sql-server-commands.txt

echo "USE $database_name;" > sql-server-commands.txt
echo "CREATE TABLE $table_name (ID INT AUTO_INCREMENT PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100), username VARCHAR(250), password VARCHAR(200));" > sql-server-commands.txt
echo "LOAD DATA LOCAL INFILE $toImportFilePath INTO TABLE $table_name FIELDS TERMINATED BY ',' IGNORE 1 ROWS;" > sql-server-commands.txt