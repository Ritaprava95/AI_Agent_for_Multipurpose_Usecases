from email.message import EmailMessage
from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, FinalAnswerTool, HfApiModel, load_tool, tool
import datetime
import requests
import pytz
import yaml

from Gradio_UI import GradioUI

# print('hemlo')

@tool
def add_number(arg1:int, arg2:int)-> str: # it's important to specify the return type
    # Keep this format for the tool description / args description but feel free to modify the tool
    """ a tool that adds 2 numbers
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return f"Addition of arg1and arg2 is {arg1+arg2}"

@tool
def write_email(topic:str, receiver:str, sender:str)->str:
    """ a tool that writes an email and returns the message
    Args:
        topic: the topic of the email
        receiver: the receiver of the email
        sender: the sender of the email
    """
    sub = topic
    msg = f"\nHi {receiver.split('@')[0]},\n\n{topic}\n\nRegards,\n{sender.split('@')[0]}"
    return msg


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

with open("system_prompt.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# print(prompt_templates)

# We're creating our CodeAgent
agent = CodeAgent(
    model=model,
    tools=[add_number, write_email, get_current_time_in_timezone, final_answer],  # add your tools here (don't remove final_answer)
    max_steps=6,
    verbosity_level=1,
    # grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

GradioUI(agent).launch()