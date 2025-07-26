from pydantic_ai import Agent
from agents.agent_latex.prompt_ import latex_expert_prompt
from dotenv import load_dotenv

load_dotenv()

def agent_latex_wrapper(topic:str):
    agente_latex = Agent(
    "deepseek:deepseek-reasoner",
    system_prompt=latex_expert_prompt())
    result = agente_latex.run(topic)
    return result

