#!/bin/sh
# Script to restore the JSON backups into the local database.

. ./common.sh

for collection in $COLLECTIONS; do
    echo "Restoring $collection"
    $IMP --db=$DB --collection $collection --drop --file $BKUP_DIR/$collection.json
done
