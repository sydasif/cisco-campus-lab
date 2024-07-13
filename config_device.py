import yaml
import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


def setup_logging(log_file):
    """
    Set up logging configuration.

    Args:
        log_file (str): The file where logs will be saved.
    """
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')


def load_config(config_file, device_name):
    """
    Load configuration from a YAML file.

    Args:
        config_file (str): The path to the YAML configuration file.
        device_name (str): The name of the device to configure.

    Returns:
        tuple: A tuple containing the device configuration and the list of commands.
    """
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        device = config[device_name]
        commands = config['commands']
    return device, commands


def configure_device(device, commands):
    """
    Configure a network device with the specified commands.

    Args:
        device (dict): The device connection parameters.
        commands (list): The list of configuration commands.
    """
    try:
        # Connect to the device
        logging.info(f"Connecting to {device['host']}")
        net_connect = ConnectHandler(**device)

        # Apply the configuration commands
        logging.info("Sending configuration commands")
        output = net_connect.send_config_set(commands)
        logging.info(output)

        # Save the configuration
        logging.info("Saving the configuration")
        net_connect.save_config()

        # Disconnect from the device
        net_connect.disconnect()
        logging.info("Disconnected from the device")

    except NetmikoTimeoutException as e:
        logging.error(f"Timeout while connecting to the device: {e}")
    except NetmikoAuthenticationException as e:
        logging.error(f"Authentication failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# If the module is executed as the main script
if __name__ == "__main__":
    # Get user inputs for the configuration file, device name, and log file
    config_file = input("Enter YAML file name: ")
    device_name = input("Device name to config: ")
    log_file = device_name + '.log'

    # Set up logging
    setup_logging(log_file)

    # Load the device configuration and commands
    device, commands = load_config(config_file, device_name)

    # Configure the device
    configure_device(device, commands)
