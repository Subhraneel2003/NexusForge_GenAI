# agents/developer.py
from crewai import Agent, Task
from agents import BaseAgent

class DeveloperAgent(BaseAgent):
    """Developer agent responsible for creating code based on design and user stories"""
    
    def _create_agent(self):
        return Agent(
            role="Software Developer",
            goal="Write clean, efficient, and maintainable code that implements the design specifications",
            backstory="""You are a skilled Software Developer with expertise in multiple 
            programming languages and frameworks. You write clean, well-documented code 
            that follows best practices and is easy to maintain. You have a keen eye for 
            detail and are adept at translating designs into working software.""",
            verbose=True,
            llm=self.llm
        )
        
    def create_implementation_task(self, user_stories, design_doc):
        """Create a task to implement code based on user stories and design"""
        return Task(
            description=f"""
            Implement code based on the following user stories and design document:
            
            === USER STORIES ===
            {user_stories}
            
            === DESIGN DOCUMENT ===
            {design_doc}
            
            Create working code that implements the functionality described in the user 
            stories according to the specifications in the design document. Your implementation 
            should:
            
            1. Follow clean code principles
            2. Include appropriate error handling
            3. Be well-documented with comments
            4. Include unit tests for key functionality
            5. Follow the architectural patterns specified in the design
            
            Focus on implementing one component at a time, starting with the core functionality.
            """,
            agent=self.agent,
            expected_output="Working code implementing the specified functionality"
        )
        
    def create_code_review_task(self, code, feedback=None):
        """Create a task to review and refine code based on feedback"""
        feedback_section = ""
        if feedback:
            feedback_section = f"""
            Consider the following feedback in your review:
            
            {feedback}
            """
            
        return Task(
            description=f"""
            Review the following code implementation:
            
            {code}
            
            {feedback_section}
            
            Perform a thorough code review, looking for:
            1. Bugs or logical errors
            2. Performance issues
            3. Security vulnerabilities
            4. Adherence to best practices
            5. Completeness of implementation
            6. Test coverage
            
            Provide specific suggestions for improvements and fix any issues you identify.
            Return the improved version of the code with comments explaining your changes.
            """,
            agent=self.agent,
            expected_output="Improved code with explanatory comments"
        )