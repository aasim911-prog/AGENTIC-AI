 
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search

GEMINI_MODEL = "gemini-2.0-flash"

 # Researcher 1: Renewable Energy
researcher_agent_1 = LlmAgent(
     name="RenewableEnergyResearcher",
     model=GEMINI_MODEL,
     instruction="""You are an AI Research Assistant specializing in energy.
 Research the latest advancements in 'renewable energy sources'.
 Use the Google Search tool provided.
 Summarize your key findings concisely (1-2 sentences).
 Output *only* the summary.
 """,
     description="Researches renewable energy sources.",
     tools=[google_search],
     # Store result in state for the merger agent
     output_key="renewable_energy_result"
 )

 # Researcher 2: Electric Vehicles
researcher_agent_2 = LlmAgent(
     name="EVResearcher",
     model=GEMINI_MODEL,
     instruction="""You are an AI Research Assistant specializing in transportation.
 Research the latest developments in 'electric vehicle technology'.
 Use the Google Search tool provided.
 Summarize your key findings concisely (1-2 sentences).
 Output *only* the summary.
 """,
     description="Researches electric vehicle technology.",
     tools=[google_search],
     # Store result in state for the merger agent
     output_key="ev_technology_result"
 )

 # Researcher 3: Carbon Capture
researcher_agent_3 = LlmAgent(
     name="CarbonCaptureResearcher",
     model=GEMINI_MODEL,
     instruction="""You are an AI Research Assistant specializing in climate solutions.
 Research the current state of 'carbon capture methods'.
 Use the Google Search tool provided.
 Summarize your key findings concisely (1-2 sentences).
 Output *only* the summary.
 """,
     description="Researches carbon capture methods.",
     tools=[google_search],
     # Store result in state for the merger agent
     output_key="carbon_capture_result"
 )

 