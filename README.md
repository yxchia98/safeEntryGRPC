# safeEntryGRPC

To intialize MongoDB container with initial records:

```
docker-compose up
```

To setup mongodb container(OLD DONT USE):

```
docker run --name safe-entry-mongo -d -p 27017:27017 --network bridge -e MONGO_INITDB_ROOT_USERNAME=adminuser -e MONGO_INITDB_ROOT_PASSWORD=csc3004 yxchia98/safe-entry-mongo
```
