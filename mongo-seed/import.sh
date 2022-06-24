chmod +x mongo-seed/import.sh
mongoimport -u adminuser -p csc3004 --host safe-entry-mongo --authenticationDatabase admin --db safe-entry --collection records --type csv --file /mongo-seed/records.csv --headerline
