# safeEntryGRPC

Provision MongoDB container with initial records:

```
docker-compose up
```

Start gRPC server:

```
python .\safe_entry_server.py
```

Start gRPC main client:

```
python .\safe_entry_client.py
```

Start gRPC server:

```
python .\special_access_client.py
```

To backup entire MongoDB database:

```
docker exec -i safeentrygrpc_safe-entry-mongo_1 /usr/bin/mongodump -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --out /dump
docker cp safeentrygrpc_safe-entry-mongo_1:/dump ./mongo-seed/
```

To backup individual collections

```
docker exec -i safeentrygrpc_safe-entry-mongo_1 mongoexport -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --collection records --type=csv --fields _id,name,nric,location,checkInTime,checkOutTime --out ./dump/records.csv
docker exec -i safeentrygrpc_safe-entry-mongo_1 mongoexport -u adminuser -p csc3004 --authenticationDatabase admin --db safe-entry --collection clusters --type=csv --fields _id,location,time --out ./dump/clusters.csv
docker cp safeentrygrpc_safe-entry-mongo_1:/dump/records.csv ./mongo-seed
docker cp safeentrygrpc_safe-entry-mongo_1:/dump/clusters.csv ./mongo-seed
```
