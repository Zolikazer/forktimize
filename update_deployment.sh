set -e

echo "Pulling latest code..."
git reset --hard origin/master
git clean -fd
git pull

echo "Stopping old containers..."
docker compose down

echo "Rebuilding and starting new containers..."
docker compose up -d --build --remove-orphans

echo "Cleaning up old Docker images..."
docker system prune -a -f

echo "Deployment complete!"