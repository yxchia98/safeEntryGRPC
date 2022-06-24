# safeEntryGRPC

To intialize MongoDB container with initial records:

```
docker-compose up
```

To backup MongoDB records:

```
# to backup entire database
docker exec -i safeentrygrpc_safe-entry-mongo_1 /usr/bin/mongodump -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --out /dump
docker cp safeentrygrpc_safe-entry-mongo_1:/dump ./mongo-seed
# to backup individual collections
docker exec -i safeentrygrpc_safe-entry-mongo_1 mongoexport -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --collection records --type=csv --fields _id,name,nric,location,checkInTime,checkOutTime --out ./dump/records.csv
docker exec -i safeentrygrpc_safe-entry-mongo_1 mongoexport -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --collection clusters --type=csv --fields _id,location,time --out ./dump/clusters.csv
docker cp safeentrygrpc_safe-entry-mongo_1:/dump/clusters.csv ./mongo-seed
```

To setup mongodb container(OLD DONT USE):

```
docker run --name safe-entry-mongo -d -p 27017:27017 --network bridge -e MONGO_INITDB_ROOT_USERNAME=adminuser -e MONGO_INITDB_ROOT_PASSWORD=csc3004 yxchia98/safe-entry-mongo
```
