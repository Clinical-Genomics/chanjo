##
# Chanjo
#
# @file
# @version 0.1

.DEFAULT_GOAL := help
.PHONY: build run init prune help up down bash-chanjo

build:    ## Build new images
	docker-compose build
init:    ## Initialize database and load demo data
	echo "Setup chanjo database"
	docker-compose run chanjo-cli /bin/bash -c "chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test init --auto demodata && chanjo --config demodata/chanjo.yaml link demodata/hgnc.grch37p13.exons.bed"
	echo "Loading coverage from demo files"
	docker-compose run chanjo-cli chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test load chanjo/init/demo-files/sample1.coverage.bed
	docker-compose run chanjo-cli chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test load chanjo/init/demo-files/sample2.coverage.bed
	docker-compose run chanjo-cli chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test load chanjo/init/demo-files/sample3.coverage.bed

calculate: ## Simple command to calculate mean over data stored in database
	echo "Calculate mean coverage"
	docker-compose run chanjo-cli chanjo -d mysql+pymysql://chanjoUser:chanjoPassword@mariadb/chanjo4_test calculate mean

prune: ## Remove orphans and dangling images
	docker-compose down --remove-orphans
	docker images prune
help:    ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# end
