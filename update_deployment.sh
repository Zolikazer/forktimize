set -e

echo "Pulling latest code..."
git pull origin master

echo "Stopping old containers..."
docker compose down

echo "Rebuilding and starting new containers..."
docker compose up -d --build

echo "Cleaning up old Docker images..."
docker image prune -f

echo "Deployment complete!"