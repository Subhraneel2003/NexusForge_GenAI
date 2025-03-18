# agents/tester.py
from crewai import Agent, Task
from agents import BaseAgent

class TesterAgent(BaseAgent):
    """Tester agent responsible for creating and executing test cases"""
    
    def _create_agent(self):
        return Agent(
            role="Quality Assurance Tester",
            goal="Ensure software quality through comprehensive testing",
            backstory="""You are a meticulous Quality Assurance Tester with an eye for detail 
            and a passion for finding edge cases. You understand the importance of both 
            functional and non-functional testing. You create thorough test plans that cover 
            all aspects of the software and help identify issues before they reach production.""",
            verbose=True,
            llm=self.llm
        )
        
    def create_test_plan_task(self, user_stories, design_doc):
        """Create a task to generate a test plan based on user stories and design"""
        return Task(
            description=f"""
            Based on the following user stories and design document, create a comprehensive test plan:
            
            === USER STORIES ===
            {user_stories}
            
            === DESIGN DOCUMENT ===
            {design_doc}
            
            Your test plan should include:
            
            1. Test Strategy
               - Testing approach (manual, automated, hybrid)
               - Testing levels (unit, integration, system, acceptance)
               - Testing environment requirements
               
            2. Test Cases
               - For each user story, create 3-5 test cases
               - Each test case should have:
                 * Unique identifier (TC-XXX)
                 * Description
                 * Preconditions
                 * Test steps
                 * Expected results
                 * Priority (Critical, High, Medium, Low)
                 
            3. Non-functional Test Cases
               - Performance tests
               - Security tests
               - Usability tests
               
            4. Test Data Requirements
               - Data needed for each test case
               
            Ensure your test cases cover happy paths, edge cases, and error scenarios.
            """,
            agent=self.agent,
            expected_output="A comprehensive test plan with detailed test cases"
        )
        
    def execute_tests_task(self, test_plan, code):
        """Create a task to execute tests against the implemented code"""
        return Task(
            description=f"""
            Execute the following test plan against the implemented code:
            
            === TEST PLAN ===
            {test_plan}
            
            === CODE ===
            {code}
            
            For each test case in the test plan:
            1. Analyze if the test would pass or fail based on the code implementation
            2. Provide detailed reasoning for your assessment
            3. For failing tests, identify the specific issue in the code
            
            Compile your findings into a test execution report that includes:
            1. Test execution summary (total tests, passed, failed)
            2. Detailed results for each test case
            3. Bugs and issues identified
            4. Recommendations for fixing issues
            """,
            agent=self.agent,
            expected_output="A detailed test execution report"
        )