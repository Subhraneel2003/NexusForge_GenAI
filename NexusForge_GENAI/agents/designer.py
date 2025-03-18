# agents/designer.py
from crewai import Agent, Task
from agents import BaseAgent

class DesignerAgent(BaseAgent):
    """Designer agent responsible for creating software design documentation"""
    
    def _create_agent(self):
        return Agent(
            role="Software Designer",
            goal="Create comprehensive and implementable software designs",
            backstory="""You are an experienced Software Designer with expertise in 
            creating clean, modular, and scalable architectures. You understand design 
            patterns, best practices, and how to balance technical constraints with 
            business requirements.""",
            verbose=True,
            llm=self.llm
        )
        
    def create_design_task(self, user_stories):
        """Create a task to generate software design based on user stories"""
        return Task(
            description=f"""
            Based on the following user stories, create a comprehensive software design:
            
            {user_stories}
            
            Your design document should include:
            
            1. System Architecture Overview
               - Components and their relationships
               - Deployment architecture
               
            2. Data Model
               - Entity relationship diagram
               - Key entities and attributes
               - Database schema recommendations
               
            3. API Design
               - Endpoints and their functionality
               - Request/response formats
               - Authentication/authorization approach
               
            4. Component Design
               - Class/module structure
               - Key interfaces and their methods
               - Design patterns applied
               
            5. Non-functional Considerations
               - Scalability approach
               - Security measures
               - Performance optimizations
               
            Be specific and provide enough detail for a developer to implement.
            """,
            agent=self.agent,
            expected_output="A comprehensive software design document"
        )
        
    def review_design_task(self, design_doc, feedback):
        """Create a task to review and refine the design based on feedback"""
        return Task(
            description=f"""
            Review the following feedback on your design document:
            
            {feedback}
            
            Based on this feedback, refine the design document:
            
            {design_doc}
            
            Address all feedback points, ensure the design is implementable, and clarify
            any ambiguous areas. Consider edge cases and potential technical challenges.
            """,
            agent=self.agent,
            expected_output="A refined design document addressing all feedback"
        )