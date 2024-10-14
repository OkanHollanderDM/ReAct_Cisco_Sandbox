import os
import json
import logging
import difflib
from typing import Dict, Union
from langchain.agents import AgentExecutor
from genie.libs.parser.utils import get_parser
from login_logout import device_connection

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

_command_cache = None


# Load supported commands
def load_supported_commands():
    global _command_cache
    if _command_cache is not None:
        return _command_cache

    file_path = os.path.join(os.path.dirname(__file__), 'commands.json')
    # check if the file exists
    if not os.path.exists(file_path):
        return {"error": "The file does not exist."}

    try:
        # Load the json file with commands
        with open(file_path, 'r') as file:
            raw_data = json.load(file)
        # Extract the commands
        _command_cache = [command['command'] for command in raw_data]
        return _command_cache
    except Exception as e:
        logger.error(f'Error loading the supported commands: {str(e)}', exc_info=True)
        return {"error": str(e)}


# Function to check if a command is supported
def check_command_support(command: str) -> Dict[str, Union[bool, str]]:
    command_list = load_supported_commands()
    if 'error' in command_list:
        return command_list

    # Find closest match
    # commands = command_list
    close_match = difflib.get_close_matches(command, command_list, n=1, cutoff=0.8)

    if close_match:
        closest_command = close_match[0]
        return {'supported': True, 'closest_command': closest_command}
    else:
        return {'supported': False}


# Process agent and chain tools
def process_agent_response(response, agent_executor: AgentExecutor):
    action = response.get('action', {})
    next_tool = action.get('next_tool')
    command_input = action.get('input')

    if response.get('status') and next_tool and command_input:
        return agent_executor.invoke({
            'input': command_input,
            'agent_scratchpad': '',
            'chat_history': response['chat_history'],
            'tool': next_tool
        })
    else:
        return response


# function to learn the configuration with pyATS
def execute_show_run():
    try:
        with device_connection() as device:
            # Execute the show run command
            logger.info('Executing show run command...')
            learned_config = device.execute('show run brief')
            return learned_config
    except Exception as e:
        logger.error(f'Error executing show run command: {str(e)}', exc_info=True)
        return {'error': str(e)}


# function to run any supported show command with pyATS
def run_show_command(command: str):
    try:
        disallowed_modifiers = ['|', 'include', 'exclude', 'begin', 'section', 'redirect', '<', '>']

        # Check if the command contains any disallowed modifiers
        for modifier in disallowed_modifiers:
            if modifier in command:
                return {'error': f'The modifier "{modifier}" is not allowed in the command.'}

        with device_connection() as device:
            # Check if the command is supported
            logger.info(f'Checking if the command {command} is supported...')
            parser = get_parser(command, device)
            if parser is None:
                return {'error': 'The command is not supported.'}

            # Execute the command
            logger.info(f'Executing the command {command}...')
            parsed_output = device.parse(command)

            return parsed_output

    except Exception as e:
        logger.error(f'Error executing the command {command}: {str(e)}', exc_info=True)
        return {'error': str(e)}


# Function to learn the logging with pyATS
def execute_show_log():
    try:
        with device_connection() as device:
            # Execute the show log command
            logger.info('Executing show log command...')
            log_output = device.execute('show logging last 250')
            return log_output
    except Exception as e:
        logger.error(f'Error executing show log command: {str(e)}', exc_info=True)
        return {'error': str(e)}
