# Warning control
from typing import Optional
import warnings
warnings.filterwarnings('ignore')
from rich.console import Console
from rich.markdown import Markdown
# Load environment variables
# from helper import load_env
# load_env()
from helpers import get_ollama_client, get_default_model

# Ollama Roles for Chat are based on the ChatGPT API roles:
# https://platform.openai.com/docs/guides/text-generation#messages-and-roles
# NOTE: `system` is now called `developer`

# https://www.baeldung.com/cs/chatgpt-api-roles
# https://devtoolhub.com/chatgpt-roles-demystified-system-user-and-assistant-explained/
"""
Ollama Chat Roles:

System – This role sets the overall behavior and rules for the AI. It provides instructions on how the model should behave, what tone to use, and what constraints to follow.
Example: "You are a helpful assistant that responds concisely."

User – This is the role of the person interacting with the AI. The user provides input, asks questions, and makes requests.
Example: "What is the capital of France?"

Assistant – This is the role the AI takes on when responding to the user. It generates replies based on the system instructions and user input.
Example: "The capital of France is Paris."

Tool – This role represents external functions or APIs that the assistant can call to retrieve or process information. Tools allow the AI to extend its capabilities beyond its built-in knowledge.
Example: A tool might fetch live weather data when the user asks, "What’s the weather like in New York?"
"""



# https://github.com/ollama/ollama/blob/main/docs/api.md
# https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
DEFAULT_CONSOLE = Console()
def mdprint(markdown: Optional[str | Markdown], /, console: Console = DEFAULT_CONSOLE, **kwargs):
    if not markdown:
        markdown = ""
    if isinstance(markdown, str):
        markdown = Markdown(markdown)
    console.print(markdown)
    

ollama = get_ollama_client()
model = get_default_model()

response = ollama.chat(
    model=model,
    messages=[
        {
            'role': 'user',  # One of: system, user, assistant, or tool
            'content': 'Why is the sky blue?',
        },
    ],
    # stream=True,
)
# response = "".join(stream)
mdprint(response.message.content)

# https://github.com/ollama/ollama/blob/main/docs/api.md#chat-request-with-history
response = ollama.chat(
    model=model,
    messages=[
        {
            'role': 'user',  # One of: system, user, assistant, or tool
            'content': 'What is meaning of the 4 ollama chat roles?',
        },
    ],
    # stream=True,
)
# response = "".join(stream)
mdprint(response.message.content)