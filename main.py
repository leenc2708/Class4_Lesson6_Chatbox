import chainlit as cl
import httpx, os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
load_dotenv()

model = OpenAIModel(
    #'deepseek/deepseek-r1-0528:free',
    #'google/gemini-2.5-flash-lite',
    'openai/gpt-oss-20b:free',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
        http_client=httpx.AsyncClient(verify=False)
    ),
)

agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'Please answer it as a traffic assistant in Hong Kong'
        'answer in brief and everything in traditional Chinese; '
    ),
)

@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", agent)

# on message do something
@cl.on_message #decorator
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    content = response.output
    msg = cl.Message(content=content)
    await msg.send()

#response = agent.run_sync("?")
#print(response.output)