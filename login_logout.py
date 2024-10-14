from pyats.topology import loader
import logging
from contextlib import contextmanager

########################
# Logging Configuration
########################
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('network_assistant.log'),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


def load_and_login():
    # Load the testbed
    testbed = loader.load('testbed.yaml')
    # Access the device from the testbed
    device = testbed.devices['Cat8000V']
    try:
        # Connect to the device
        logger.info('Connecting to the device...')
        device.connect()
        return device
    except Exception as e:
        logger.error(f'Error connecting to the device: {str(e)}', exc_info=True)
        raise e


@contextmanager
def device_connection():
    device = None
    try:
        device = load_and_login()
        yield device
    finally:
        if device:
            print('Disconnecting from the device...')
            device.disconnect()
