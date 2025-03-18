# agents/business_analyst.py
from crewai import Agent, Task
from agents import BaseAgent

class BusinessAnalystAgent(BaseAgent):
    """Business Analyst agent responsible for creating user stories"""
    
    def _create_agent(self):
        return Agent(
            role="Business Analyst",
            goal="Create detailed user stories that accurately capture business requirements",
            backstory="""You are a skilled Business Analyst with expertise in translating 
            business needs into clear, actionable user stories. You have a knack for asking 
            the right questions and ensuring requirements are specific, measurable, achievable, 
            relevant, and time-bound.""",
            verbose=True,
            llm=self.llm
        )
        
    def create_user_stories_task(self, project_init_doc):
        """Create a task to generate user stories from project requirements"""
        return Task(
            description=f"""
            Based on the following project initialization document, create detailed user stories:
            
            {project_init_doc}
            
            For each epic identified in the project initialization document, create 2-5 user 
            stories following the format:
            
            "As a [user role], I want [action/feature] so that [benefit/value]."
            
            Each user story should include:
            1. A unique identifier (US-XXX)
            2. Acceptance criteria (3-5 specific conditions)
            3. Story points estimation (1, 2, 3, 5, 8, 13)
            4. Priority (Critical, High, Medium, Low)
            5. Dependencies (if any)
            
            Organize the user stories by epic and ensure coverage of all requirements.
            """,
            agent=self.agent,
            expected_output="A set of well-defined user stories organized by epic"
        )
        
    def refine_user_stories_task(self, user_stories, feedback):
        """Create a task to refine user stories based on feedback"""
        return Task(
            description=f"""
            Review the following feedback on your user stories:
            
            {feedback}
            
            Based on this feedback, refine the user stories:
            
            {user_stories}
            
            Ensure each user story is now more detailed, specific, and actionable.
            Address all feedback points and improve clarity where needed.
            """,
            agent=self.agent,
            expected_output="A set of refined user stories addressing all feedback"
        )