from langchain_ollama.llms import OllamaLLM
from langchain_core.tools import tool, render_text_description, BaseTool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import traceback

from commands import process_agent_response
from template import template
from tools import TOOLS
import logging

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

llm = OllamaLLM(model="llama3.1")
tools = [tool for tool in TOOLS if isinstance(tool, BaseTool)]
tool_description = render_text_description(tools)
input_variables = ['input', 'agent_scratchpad', 'chat_history']
prompt_template = PromptTemplate(
    template=template,
    input_variables=input_variables,
    partial_variables={
        'tools': tool_description,
        'tool_names': ', '.join([tool.name for tool in tools])
    }
)
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               handle_parsing_errors=True,
                               verbose=True,
                               max_iterations=5)


########################
# Main Function
########################
def main():
    # Initialize chat history
    chat_history = []

    while True:
        # Get User input
        user_input = input('Enter your question (or type "exit" to quit): ')

        if user_input.lower() == 'exit':
            logger.info('Exiting...')
            break

        # Add user input to the chat history
        chat_history.append(f'User: {user_input}')

        # Create the agent input with the required structure
        agent_input = {
            'input': user_input,
            'agent_scratchpad': '',
            'chat_history': '\n'.join(chat_history),
        }

        # Execute the agent with the given input
        try:
            response = agent_executor.invoke(agent_input)

            # Process the agent response
            response_processed = process_agent_response(response, agent_executor)

            # Add the agent response to the chat history
            chat_history.append(f'Agent: {response_processed}')

            print(response_processed)
        except Exception as e:
            logger.error(f'Error: {str(e)}', exc_info=True)
            traceback.print_exc()


if __name__ == '__main__':
    logger.info('Starting the Network Assistant...')
    main()
