# agents/__init__.py
from langchain.schema import SystemMessage
from crewai import Agent

class BaseAgent:
    """Base class for all agents in the virtual development pod"""
    
    def __init__(self, llm):
        self.llm = llm
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """Create the CrewAI agent - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")
        
    def get_agent(self):
        """Return the CrewAI agent"""
        return self.agent