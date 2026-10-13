#!/bin/sh
# Some common shell stuff.
# Run the scripts that use this from the data/ directory.

echo "Importing from common.sh"

# Must match SE_DB in db_connect.py.
DB=seDB
if [ -z $DATA_DIR ]
then
    DATA_DIR=$(pwd)
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=mongoexport
IMP=mongoimport

# Every collection in the app's database. A plain string rather than an
# array, because /bin/sh on Ubuntu (dash) doesn't support arrays.
COLLECTIONS="states counties areas vaccination_sites candidate_sites campaigns mobile_units deployments"
