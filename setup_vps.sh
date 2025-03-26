#!/bin/bash

set -e  # Stop on errors

echo "🔥 Setting up Forktimize VPS..."

# ✅ Update system and install Docker
echo "📦 Installing Docker..."
sudo apt update && sudo apt upgrade -y
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo apt install -y vim htop rsync sqlite3

# ✅ Clone the repo if missing
if [ ! -d "/opt/forktimize" ]; then
    echo "🛠 Cloning Forktimize repo..."
    sudo mkdir /opt/forktimize
    sudo chown -R $USER:$USER /opt/forktimize
    git clone https://github.com/zolikazer/forktimize.git /opt/forktimize
else
    echo "✅ Repo exists, skipping clone."
fi

cd /opt/forktimize

sudo bash -c "cat > /tmp/ngnix.conf" <<EOF
events {}

http {
server {
    listen 80;
    server_name forktimize.xyz;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type "text/plain";
        try_files $uri =404;
    }

    # Optional: reject everything else
    location / {
        return 404;
    }
}
}

EOF

# ✅ Start a standalone NGINX container for Certbot HTTP challenge
echo "🌍 Starting NGINX for Certbot verification..."
sudo docker run -d --name certbot-nginx -p 80:80 \
  -v "/var/www/certbot:/var/www/certbot" \
  -v "/tmp/ngnix.conf:/etc/nginx/nginx.conf:ro" \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  nginx:latest

# ✅ Run Certbot inside a temporary container
echo "🔐 Requesting SSL certificate..."
sudo docker run --rm \
  -v "/var/www/certbot:/var/www/certbot" \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d forktimize.xyz --non-interactive --agree-tos --email okoskacsaka@gmail.com

# ✅ Stop and remove temporary NGINX container
echo "🛑 Stopping temporary NGINX..."
sudo docker stop certbot-nginx
sudo docker rm certbot-nginx

# ✅ Bring up everything with Docker Compose (Final Setup)
echo "🚀 Starting full deployment..."
sudo docker compose up -d --build

echo "🎉 Forktimize is fully set up with SSL!"
