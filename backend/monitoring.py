import logging

# Configure basic logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO  # Change to DEBUG for more details
)

logger = logging.getLogger(__name__)
