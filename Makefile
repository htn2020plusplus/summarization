.DEFAULT_GOAL := help

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## run local
	cd transformer && python pipeline.py
d-build: ## build docker
	cd transformer && docker build . -t legist-summarizer:latest
d-run: ## run docker
	docker run legist-summarizer:latest