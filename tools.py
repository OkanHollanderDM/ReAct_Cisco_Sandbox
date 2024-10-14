from langchain_core.tools import tool
from commands import run_show_command, check_command_support, execute_show_run, execute_show_log
from typing import List, Callable, Any


########################
# Tools
########################
@tool
def run_show_command_tool(command: str) -> dict:
    """Execute a 'show' command on the device using pyATS and return the json output"""
    return run_show_command(command)


@tool
def check_supported_commands_tool(command: str) -> dict:
    """Check if a command is supported by the device"""
    return check_command_support(command)


@tool
def learn_configuration_tool() -> dict:
    """Learn the configuration of the device using the 'show run brief' command"""
    return execute_show_run()


@tool
def learn_logging_tool() -> dict:
    """Learn the logging of the device using the 'show logging last 250' command"""
    return execute_show_log()


TOOLS: List[Callable[..., Any]] = [run_show_command_tool,
                                   check_supported_commands_tool,
                                   learn_configuration_tool,
                                   learn_logging_tool]
