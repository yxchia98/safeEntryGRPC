chmod +x mongo-seed/import.sh
/usr/bin/mongorestore -u adminuser -p csc3004 --host safe-entry-mongo --authenticationDatabase admin --db safe-entry /mongo-seed/dump/safe-entry
# mongoimport -u adminuser -p csc3004 --host safe-entry-mongo --authenticationDatabase admin --db safe-entry --collection records --type csv --file /mongo-seed/records.csv --headerline
# mongoimport -u adminuser -p csc3004 --host safe-entry-mongo --authenticationDatabase admin --db safe-entry --collection clusters --type csv --file /mongo-seed/clusters.csv --headerline
