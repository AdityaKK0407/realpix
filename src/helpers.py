import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout
)

logger = logging.getLogger(__name__)