#!/bin/sh

# Exit on error
set -e

# Dump wq configuration object to file
db/manage.py dump_config --format amd > app/js/data/config.js

# Build javascript with wq.app
cd app;
wq build $1;

# Force important files through any unwanted server caching
cd ../;
sed -i "s/atlasbiowork.js/atlasbiowork.js?v="$1"/" htdocs-build/atlasbiowork.appcache
sed -i "s/atlasbiowork.css/atlasbiowork.css?v="$1"/" htdocs-build/atlasbiowork.appcache

# Preserve Django's static files (e.g. admin)
if [ -d htdocs/static ]; then
    cp -a htdocs/static htdocs-build/static
fi;

# Replace existing htdocs with new version
rm -rf htdocs;
mv -i htdocs-build/ htdocs;

# Restart Django
touch db/atlasbiowork/wsgi.py
