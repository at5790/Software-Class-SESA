#!/bin/sh
# Script to backup production database to JSON files.
# MONGO_URI must hold the cloud connection string (see .env.example).

. ./common.sh

if [ -z "$MONGO_URI" ]
then
    echo "You must set MONGO_URI in your env before running this script."
    exit 1
fi

for collection in $COLLECTIONS; do
    echo "Backing up $collection"
    $EXP --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json --uri="$MONGO_URI"
done

git add $BKUP_DIR/*.json
git add $BKUP_DIR/*.json
git commit $BKUP_DIR/*.json -m "Mongo DB backup"
git pull origin master
git push origin master
