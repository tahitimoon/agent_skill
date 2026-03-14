import os
from dotenv import load_dotenv
from strands import Agent, AgentSkills
from strands.models.openai import OpenAIModel

load_dotenv()

model = OpenAIModel(
    client_args={"api_key": os.getenv("OPENAI_API_KEY")},
    model_id="gpt-5-mini",
)


plugin = AgentSkills(skills="./skills/")

agent = Agent(model=model, plugins=[plugin])

agent("hello")
