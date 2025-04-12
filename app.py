from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure APM

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-app',
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'development',
    'CAPTURE_BODY': 'all',
    'CAPTURE_HEADERS': True,
    'METRICS_INTERVAL': '15s',
    'TRANSACTION_SAMPLE_RATE': 1.0,  # Ensure 100% sampling
    'VERIFY_SERVER_CERT': False,     # Skip SSL verification if needed
    'DEBUG': True                    # Enable debug logging
}

# Initialize APM
apm = ElasticAPM(app)

@app.route('/')
def home():
    logger.info("Home endpoint called")
    return jsonify({"status": "ok", "message": "Flask app with APM integration"})

@app.route('/slow')
def slow_endpoint():
    with elasticapm.capture_span(name="sleep-operation", span_type="app"):
        logger.info("Slow endpoint called - going to sleep")
        time.sleep(random.uniform(0.1, 0.5))
    
    return jsonify({"status": "ok", "message": "Slow operation completed"})

@app.route('/error')
def error_endpoint():
    logger.error("Error endpoint called - raising exception")
    raise Exception("This is a test exception for APM")

@app.route('/custom-metric')
def custom_metric():
    # Add custom context
    elasticapm.set_custom_context({
        "custom_key": "custom_value"
    })

    # Set transaction name explicitly
    elasticapm.set_transaction_name("custom-metric-transaction")

    # Add labels/tags
    elasticapm.label(custom_label="test_value")

    logger.info("Custom metric endpoint called")
    return jsonify({"status": "ok", "message": "Custom metric recorded"})

@app.route('/transaction')
def transaction_endpoint():
    # Set transaction name
    elasticapm.set_transaction_name("custom-named-transaction")

    # Add custom context
    elasticapm.set_custom_context({
        "transaction_type": "custom",
        "importance": "high",
        "user_id": "test-user-123"
    })

    # Add labels/tags
    elasticapm.label(transaction_category="API", priority="high")

    # Simulate span work
    with elasticapm.capture_span("database-operation"):
        logger.info("Simulating database work")
        time.sleep(0.1)

    with elasticapm.capture_span("api-call"):
        logger.info("Simulating external API call")
        time.sleep(0.2)

    logger.info("Transaction endpoint completed")
    return jsonify({"status": "ok", "message": "Transaction recorded with all details"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
