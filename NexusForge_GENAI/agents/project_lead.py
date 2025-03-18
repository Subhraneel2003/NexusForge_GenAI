# agents/project_lead.py
from crewai import Agent, Task
from agents import BaseAgent

class ProjectLeadAgent(BaseAgent):
    """Project Lead agent responsible for coordinating the development pod"""
    
    def _create_agent(self):
        return Agent(
            role="Project Lead",
            goal="Coordinate the development team to deliver high-quality software on time",
            backstory="""You are an experienced Project Lead with a track record of 
            delivering successful projects. You excel at coordinating team members, 
            setting priorities, and ensuring quality standards are met.""",
            verbose=True,
            llm=self.llm,
            allow_delegation=True
        )
        
    def create_initialization_task(self, requirements):
        """Create a task to initialize the project based on requirements"""
        return Task(
            description=f"""
            Review the following business requirements and initialize the project:
            
            {requirements}
            
            Break down these requirements into high-level epics and identify the key
            deliverables. Determine the project scope, timeline, and key milestones.
            
            Output a project initialization document with:
            1. Project scope
            2. High-level epics
            3. Key deliverables
            4. Initial timeline
            5. Risk assessment
            """,
            agent=self.agent,
            expected_output="A comprehensive project initialization document"
        )
        
    def create_status_check_task(self, artifacts=None):
        """Create a task to check project status"""
        artifacts_summary = "No artifacts available yet."
        if artifacts:
            artifacts_summary = "\n".join([f"- {k}: {v}" for k, v in artifacts.items()])
            
        return Task(
            description=f"""
            Review the current project status based on the following artifacts:
            
            {artifacts_summary}
            
            Provide a status report including:
            1. Overall project health (Green/Yellow/Red)
            2. Current progress percentage
            3. Key accomplishments
            4. Blockers or risks
            5. Next steps
            """,
            agent=self.agent,
            expected_output="A concise project status report"
        )