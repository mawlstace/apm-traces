# APM Traces

## Overview
This repository contains a simple Flask application that sends traces to Elasticsearch using Elastic APM. The traces are captured and can be viewed in Kibana's APM UI.

## Setup and Running

### Prerequisites
- Docker and Docker Compose
- Elasticsearch and Kibana (included in docker-compose)
- Python 3.x

### Python and Virtual Environment Setup

1. Install Python 3.x if not already installed:
```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# For macOS (using Homebrew)
brew install python

# For Windows
# Download from https://www.python.org/downloads/
```

2. Create a virtual environment:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone this repository
2. Set up Python virtual environment (as described above)
3. Start the application with Docker Compose:
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### Volume Issues
If you encounter problems with volumes when restarting the application, you may need to prune Docker volumes:

```bash
docker volume prune -f
```

This removes unused volumes and allows the application to start with a clean state.

#### APM Server Installation
You might need to install the APM server integration from the Kibana UI. However, this step is often unnecessary as the integration should be included in the docker-compose setup.

### Verifying Traces
Once the application is running correctly, traces will be captured and stored in Elasticsearch. You can view these traces in the Kibana APM UI by navigating to:

1. Open Kibana (usually at http://localhost:5601)
2. Navigate to Observability → APM
3. Select your service from the Services list


### using split_index.text

there is elastic limitation for spliting the index from traces-apm-default to traces-apm-servicename-default where servicename is your application name 
the idea was to increase the performance of the elasticsearch under heavy apm indices however the elasticsearch has limitation to split from default index 
however the new indices can be created but the traces cant be seen in ui 

