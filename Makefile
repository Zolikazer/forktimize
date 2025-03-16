SHELL := /bin/bash

VPS_USER := spazo
VPS_HOST := forktimize
REMOTE_DIR := /opt/forktimize/
LOCAL_DIR := .backend/

run-frontend-dev:
	cd frontend;npm run dev

run-frontend:
	cd frontend;VITE_RUN_MOCK_BACKEND=false npm run dev

run-backend:
	cd backend; source .venv/bin/activate; uvicorn main:app --reload

run:
	tmux new-session -d -s city-food-planner "cd backend && . .venv/bin/activate && uvicorn main:app --reload"
	tmux split-window -h "cd frontend && VITE_RUN_MOCK_BACKEND=false npm run dev"
	tmux select-pane -t 0
	tmux attach-session -t city-food-planner

test-frontend:
	cd frontend;npm run test

test-backend:
	cd backend;source .venv/bin/activate;python -m unittest discover

test-unit: test-backend
	$(MAKE) test-frontend

e2e-test:
	cd frontend && npm run test:e2e

test-e2e:
	$(MAKE) run-backend &
	$(MAKE) run-frontend &
	sleep 5  # Give some time for the servers to start
	$(MAKE) e2e-test

deploy-backend:
	ssh ${VPS_HOST} "cd ${REMOTE_DIR} && sudo ${REMOTE_DIR}update_deployment.sh"

live-patch:
	rsync -rv backend spazo@forktimize:/opt/forktimize/ --exclude='.git' --exclude='__pycache__' --exclude='logs' --exclude="foods.db" --exclude=".venv" --exclude=".pytest_cache" --exclude=".idea" --rsync-path="sudo rsync"
	ssh $(VPS_USER)@$(VPS_HOST) "cd ${REMOTE_DIR} && sudo docker compose restart forktimize-backend"