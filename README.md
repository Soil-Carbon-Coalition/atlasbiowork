# atlasbiowork
Built on wq framework. For entering georeferenced data on landscape function with flexible, ad hoc forms using JSON field. 
### Installation

Tested on a Digital Ocean droplet running Ubuntu 15.10.

1. Fork this repository (optional)

2. Install System Dependencies:
    ```bash
    sudo apt-get update
    sudo apt-get install apache2 libapache2-mod-wsgi-py3 postgresql-9.4-postgis-2.1 python3-pip python3-psycopg2
    sudo apt-get install nodejs-legacy
    sudo apt-get install git vim python3-pil libxslt-dev libz-dev
    ```

3. Install code
    ```bash
    # Clone codebase
    cd /var/www
    sudo mkdir atlasbiowork
    sudo chown `whoami` atlasbiowork
    cd atlasbiowork
    # (Replace HTTPS URL with your fork and/or a SSH URL)
    git clone https://github.com/Soil-Carbon-Coalition/atlasbiowork .
    sudo chown www-data media
    
    # Install python dependencies
    sudo pip3 install -r requirements.txt

    # Configure local settings
    cd db/atlasbiowork
    cp local_settings.py.template local_settings.py
    vim local_settings.py  # customize SECRET_KEY
    ```

4. Initialize Database
    ```bash
    # (edit /etc/postgresql/9.4/main/pg_hba.conf and/or pg_ident.conf to set permissions)
    sudo service postgresql restart
    createuser -Upostgres atlasbiowork
    createdb -Upostgres -Oatlasbiowork atlasbiowork
    psql -Upostgres atlasbiowork -c "create extension postgis"
    cd /var/www/atlasbiowork/db
    ./manage.py migrate
    ./manage.py createsuperuser
    ```

5. Configure Apache
    ```bash
    sudo a2enmod expires ssl
    # (edit /var/www/atlasbiowork/conf/atlasbiowork.conf to ensure proper path to SSL certificate file)
    sudo ln -s /var/www/atlasbiowork/conf/atlasbiowork.conf /etc/apache2/sites-available/
    sudo a2ensite atlasbiowork
    sudo service apache2 restart
    ```
6. Clean up some details
    ```bash
	# Make sure ssl is configured properly with certificates and keys
	./manage.py collectstatic #(gives css to admin interface etc.)
	# now you can add users etc. via admin interface
	cd ..
	./deploy.sh .01 #performs the wq build process and deploys app
	```