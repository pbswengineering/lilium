# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#
# Makefile
# ~~~~~~~~
#
# Commands to interact with the production environment.
# They require a suitably configured Unix-like environment.
#
# :copyright: (c) 2018 Paolo Paolo Bernardi.
# :license: GNU AGPL version 3, see LICENSE for more details.
#

.PHONY: help install clonedb

# Passwords and security-sensitive settings are here
include Makefile.local

help:
	@echo 'Available targets:'
	@echo '   * install                    Deploy Lilium to the production server'
	@echo '   * clonedb                    Clone the production MySQL/MariaDB database to the local machine'

install:
	rsync -av -e "ssh -p $(prod_ssh_port)" --delete .  \
	--exclude db.sqlite3 \
	--exclude local_settings.py \
	--exclude logs \
	--exclude __pycache__ \
	--exclude .idea \
	--exclude venv \
	$(prod_ssh_user)@$(prod_ssh_host):$(prod_ssh_directory)

clonedb:
	ssh -p $(prod_ssh_port) $(prod_ssh_user)@$(prod_ssh_host) \
	'($(prod_mysqldump) --databases -h $(prod_mysqlhost) -u $(prod_mysqluser) --password=$(prod_mysqlpass) $(prod_mysqldb) | gzip)' | \
	gunzip | \
	mysql -h $(local_mysqlhost) -u $(local_mysqluser) --password=$(local_mysqlpass)

checkdb:
	mysqlcheck -u $(prod_mysqluser) --password=$(prod_mysqlpass) --auto-repair ${prod_mysqldb}
