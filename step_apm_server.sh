#!/bin/bash

# Update package repository and install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg

# Add Elastic repository key
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# Add Elastic repository
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list > /dev/null

# Update apt and install apm-server
sudo apt-get update
sudo apt-get install -y apm-server

# Backup the default configuration
sudo cp /etc/apm-server/apm-server.yml /etc/apm-server/apm-server.yml.bak

# Configure APM Server
cat <<EOF | sudo tee /etc/apm-server/apm-server.yml
apm-server:
  host: "0.0.0.0:8200"
  rum:
    enabled: true
  kibana:
    enabled: true
    host: "localhost:5601"
    username: "elastic"
    password: "changeme"

output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "changeme"

logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/apm-server
  name: apm-server
  keepfiles: 7
  permissions: 0644
EOF

# Set proper permissions
sudo chown root:apm-server /etc/apm-server/apm-server.yml
sudo chmod 640 /etc/apm-server/apm-server.yml

# Enable and start APM Server
sudo systemctl daemon-reload
sudo systemctl enable apm-server
sudo systemctl start apm-server

# Check service status
echo "APM Server status:"
sudo systemctl status apm-server --no-pager

echo "APM Server has been installed and configured."
echo "APM Server is running at: http://localhost:8200"
