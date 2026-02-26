
import os
import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel
from smolagents import tool, Tool
from smolagents import VisitWebpageTool

# Read token safely
token = os.getenv("smol")  # or "HF_TOKEN"
if not token:
    raise RuntimeError("Token not found. Set it in Space → Settings → Variables")
@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion: The type of occasion for the party.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)
    
    return best_service


# Model
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=token
)

# Agent
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(),VisitWebpageTool(),
        suggest_menu,
        catering_service_tool,

	],
    model=model
)

# Function Gradio will call
def run_agent(query: str) -> str:
    return agent.run(query)

# Gradio UI
gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(
        label="Ask the agent",
        placeholder="Search for party music recommendations..."
    ),
    outputs=gr.Textbox(label="Agent response"),
    title="SmolAgents Demo (HF Spaces)"
).launch()