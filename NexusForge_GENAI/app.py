# app.py
import os
import datetime
import streamlit as st
import uuid
from dotenv import load_dotenv
from crewai import Crew, Process, Task
from database.db_manager import DatabaseManager
from config import PROJECT_MANAGER_NAME
# Import agents
from agents.project_lead import ProjectLeadAgent
from agents.business_analyst import BusinessAnalystAgent
from agents.designer import DesignerAgent
from agents.developer import DeveloperAgent
from agents.tester import TesterAgent


# Load environment variables
load_dotenv()

# Initialize database
db_manager = DatabaseManager()

# Set page configuration
st.set_page_config(
    page_title="NexusForge",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "project_id" not in st.session_state:
    st.session_state.project_id = str(uuid.uuid4())
if "artifacts" not in st.session_state:
    st.session_state.artifacts = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "initialization"

@st.cache_resource
def get_llm():
    from langchain_community.chat_models import ChatLiteLLM
    
    return ChatLiteLLM(
        model="gemini/gemini-1.5-flash",  # Correct model format for LiteLLM
        temperature=1.0,
        api_key=os.getenv("GEMINI_API_KEY")
    )

# Initialize agents
@st.cache_resource
def initialize_agents(_llm):  # Add underscore to parameter name here
    project_lead = ProjectLeadAgent(_llm)  # Use the parameter with underscore
    business_analyst = BusinessAnalystAgent(_llm)
    designer = DesignerAgent(_llm)
    developer = DeveloperAgent(_llm)
    tester = TesterAgent(_llm)
    
    return {
        "project_lead": project_lead,
        "business_analyst": business_analyst,
        "designer": designer,
        "developer": developer,
        "tester": tester
    }

# Initialize crew
def create_crew(agents, tasks):
    return Crew(
        agents=[agent.get_agent() for agent in agents.values()],
        tasks=tasks,
        verbose=True,
        process=Process.sequential
    )

# Header
#st.title("🤖 NexusForge: Advanced AI Development Framework")
st.markdown(
    "<h1 style='font-size: 40px;'>🤖 NexusForge: Advanced AI Development Framework</h1>",
    unsafe_allow_html=True
)
st.markdown("""
NexusForge is a comprehensive development framework designed to orchestrate multiple AI agents collaboratively on complex tasks within a unified ecosystem. The system leverages the CrewAI architecture to enable specialized AI agents to work in concert, each contributing unique capabilities to solve multi-faceted development challenges.
""")

# Sidebar
st.sidebar.header("Project Information")
#st.sidebar.write(f"Project ID: {st.session_state.project_id}")

current_phase = st.sidebar.selectbox(
    "Current Phase",
    ["Initialization", "Requirements", "Design", "Development", "Testing", "Review"],
    index=["initialization", "requirements", "design", "development", "testing", "review"].index(st.session_state.current_phase)
)
st.session_state.current_phase = current_phase.lower()

# Main content area
tab1, tab2, tab3 = st.tabs(["Project Management", "Artifacts", "Chat"])

# Project Management Tab
with tab1:
    st.header("Project Management")
    
    # Project initialization
    if st.session_state.current_phase == "initialization":
        st.subheader("Project Initialization")
        
        with st.form("project_init_form"):
            project_name = st.text_input("Project Name")
            project_description = st.text_area("Project Description")
            business_requirements = st.text_area("Business Requirements", height=300)
            
            submitted = st.form_submit_button("Initialize Project")
            
            if submitted and business_requirements:
                with st.spinner("Initializing project..."):
                    # Get LLM and agents
                    llm = get_llm()
                    agents = initialize_agents(llm)
                    
                    # Create initialization task
                    init_task = agents["project_lead"].create_initialization_task(business_requirements)
                    
                    # Create and run crew
                    crew = create_crew(
                        agents={"project_lead": agents["project_lead"]},
                        tasks=[init_task]
                    )
                    result = crew.kickoff()
                    
                    # Store artifact
                    artifact_id = f"project_init_{st.session_state.project_id}"
                    db_manager.store_artifact(
                        artifact_id=artifact_id,
                        artifact_content=str(result),
                        metadata={
                            "type": "project_initialization",
                            "project_id": st.session_state.project_id,
                            "name": project_name
                        }
                    )
                    
                    # Update session state
                    st.session_state.artifacts["project_initialization"] = result
                    st.session_state.current_phase = "requirements"
                    
                    st.success("Project initialized successfully!")
                    st.rerun()
    
    # Requirements Analysis
    elif st.session_state.current_phase == "requirements":
        st.subheader("Requirements Analysis")
        
        if "project_initialization" in st.session_state.artifacts:
            project_init = st.session_state.artifacts["project_initialization"]
            st.text_area("Project Initialization Document", project_init, height=200, disabled=True)
            
            if "user_stories" not in st.session_state.artifacts:
                if st.button("Generate User Stories"):
                    with st.spinner("Generating user stories..."):
                        # Get LLM and agents
                        llm = get_llm()
                        agents = initialize_agents(llm)
                        
                        # Create user stories task
                        user_stories_task = agents["business_analyst"].create_user_stories_task(project_init)
                        
                        # Create and run crew
                        crew = create_crew(
                            agents={"business_analyst": agents["business_analyst"]},
                            tasks=[user_stories_task]
                        )
                        result = crew.kickoff()
                        
                        # Store artifact
                        artifact_id = f"user_stories_{st.session_state.project_id}"
                        db_manager.store_artifact(
                            artifact_id=artifact_id,
                            artifact_content=result,
                            metadata={
                                "type": "user_stories",
                                "project_id": st.session_state.project_id
                            }
                        )
                        
                        # Update session state
                        st.session_state.artifacts["user_stories"] = result
                        
                        st.success("User stories generated successfully!")
                        st.rerun()
            else:
                user_stories = st.session_state.artifacts["user_stories"]
                st.text_area("User Stories", user_stories, height=300, disabled=True)
                
                with st.form("refine_stories_form"):
                    feedback = st.text_area("Provide feedback to refine user stories (optional)")
                    submitted = st.form_submit_button("Refine User Stories")
                    
                    if submitted and feedback:
                        with st.spinner("Refining user stories..."):
                            # Get LLM and agents
                            llm = get_llm()
                            agents = initialize_agents(llm)
                            
                            # Create refine task
                            refine_task = agents["business_analyst"].refine_user_stories_task(user_stories, feedback)
                            
                            # Create and run crew
                            crew = create_crew(
                                agents={"business_analyst": agents["business_analyst"]},
                                tasks=[refine_task]
                            )
                            result = crew.kickoff()
                            
                            # Update artifact
                            artifact_id = f"user_stories_{st.session_state.project_id}"
                            db_manager.update_artifact(
                                artifact_id=artifact_id,
                                artifact_content=result,
                                metadata={
                                    "type": "user_stories",
                                    "project_id": st.session_state.project_id,
                                    "refined": True
                                }
                            )
                            
                            # Update session state
                            st.session_state.artifacts["user_stories"] = result
                            
                            st.success("User stories refined successfully!")
                            st.rerun()
                
                if st.button("Proceed to Design Phase"):
                    st.session_state.current_phase = "design"
                    st.rerun()
    
    # Design Phase
    elif st.session_state.current_phase == "design":
        st.subheader("Design Phase")
        
        if "user_stories" in st.session_state.artifacts:
            user_stories = st.session_state.artifacts["user_stories"]
            st.expander("User Stories").text_area("Stories", user_stories, height=200, disabled=True)
            
            if "design_document" not in st.session_state.artifacts:
                if st.button("Generate Design Document"):
                    with st.spinner("Generating design document..."):
                        # Get LLM and agents
                        llm = get_llm()
                        agents = initialize_agents(llm)
                        
                        # Create design task
                        design_task = agents["designer"].create_design_task(user_stories)
                        
                        # Create and run crew
                        crew = create_crew(
                            agents={"designer": agents["designer"]},
                            tasks=[design_task]
                        )
                        result = crew.kickoff()
                        
                        # Store artifact
                        artifact_id = f"design_doc_{st.session_state.project_id}"
                        db_manager.store_artifact(
                            artifact_id=artifact_id,
                            artifact_content=result,
                            metadata={
                                "type": "design_document",
                                "project_id": st.session_state.project_id
                            }
                        )
                        
                        # Update session state
                        st.session_state.artifacts["design_document"] = result
                        
                        st.success("Design document generated successfully!")
                        st.rerun()
            else:
                design_doc = st.session_state.artifacts["design_document"]
                st.text_area("Design Document", design_doc, height=300, disabled=True)
                
                with st.form("refine_design_form"):
                    feedback = st.text_area("Provide feedback to refine design (optional)")
                    submitted = st.form_submit_button("Refine Design")
                    
                    if submitted and feedback:
                        with st.spinner("Refining design document..."):
                            # Get LLM and agents
                            llm = get_llm()
                            agents = initialize_agents(llm)
                            
                            # Create review task
                            review_task = agents["designer"].review_design_task(design_doc, feedback)
                            
                            # Create and run crew
                            crew = create_crew(
                                agents={"designer": agents["designer"]},
                                tasks=[review_task]
                            )
                            result = crew.kickoff()
                            
                            # Update artifact
                            artifact_id = f"design_doc_{st.session_state.project_id}"
                            db_manager.update_artifact(
                                artifact_id=artifact_id,
                                artifact_content=result,
                                metadata={
                                    "type": "design_document",
                                    "project_id": st.session_state.project_id,
                                    "refined": True
                                }
                            )
                            
                            # Update session state
                            st.session_state.artifacts["design_document"] = result
                            
                            st.success("Design document refined successfully!")
                            st.rerun()
                
                if st.button("Proceed to Development Phase"):
                    st.session_state.current_phase = "development"
                    st.rerun()
    
    # Development Phase
    elif st.session_state.current_phase == "development":
        st.subheader("Development Phase")
        
        if "design_document" in st.session_state.artifacts and "user_stories" in st.session_state.artifacts:
            design_doc = st.session_state.artifacts["design_document"]
            user_stories = st.session_state.artifacts["user_stories"]
            
            st.expander("Design Document").text_area("UDoc", design_doc, height=200, disabled=True)
            st.expander("User Stories").text_area("U Stories", user_stories, height=200, disabled=True)
            
            if "code_implementation" not in st.session_state.artifacts:
                if st.button("Generate Code Implementation"):
                    with st.spinner("Generating code implementation..."):
                        # Get LLM and agents
                        # Continuing the app.py file

                        # Get LLM and agents
                        llm = get_llm()
                        agents = initialize_agents(llm)
                        
                        # Create implementation task
                        implementation_task = agents["developer"].create_implementation_task(user_stories, design_doc)
                        
                        # Create and run crew
                        crew = create_crew(
                            agents={"developer": agents["developer"]},
                            tasks=[implementation_task]
                        )
                        result = crew.kickoff()
                        
                        # Store artifact
                        artifact_id = f"code_implementation_{st.session_state.project_id}"
                        db_manager.store_artifact(
                            artifact_id=artifact_id,
                            artifact_content=result,
                            metadata={
                                "type": "code_implementation",
                                "project_id": st.session_state.project_id
                            }
                        )
                        
                        # Update session state
                        st.session_state.artifacts["code_implementation"] = result
                        
                        st.success("Code implementation generated successfully!")
                        st.rerun()
            else:
                code_impl = st.session_state.artifacts["code_implementation"]
                st.text_area("Code Implementation", code_impl, height=300, disabled=True)
                
                with st.form("refine_code_form"):
                    feedback = st.text_area("Provide feedback to refine code (optional)")
                    submitted = st.form_submit_button("Refine Code")
                    
                    if submitted and feedback:
                        with st.spinner("Refining code implementation..."):
                            # Get LLM and agents
                            llm = get_llm()
                            agents = initialize_agents(llm)
                            
                            # Create code review task
                            review_task = agents["developer"].create_code_review_task(code_impl, feedback)
                            
                            # Create and run crew
                            crew = create_crew(
                                agents={"developer": agents["developer"]},
                                tasks=[review_task]
                            )
                            result = crew.kickoff()
                            
                            # Update artifact
                            artifact_id = f"code_implementation_{st.session_state.project_id}"
                            db_manager.update_artifact(
                                artifact_id=artifact_id,
                                artifact_content=result,
                                metadata={
                                    "type": "code_implementation",
                                    "project_id": st.session_state.project_id,
                                    "refined": True
                                }
                            )
                            
                            # Update session state
                            st.session_state.artifacts["code_implementation"] = result
                            
                            st.success("Code implementation refined successfully!")
                            st.rerun()
                
                if st.button("Proceed to Testing Phase"):
                    st.session_state.current_phase = "testing"
                    st.rerun()
    
    # Testing Phase
    elif st.session_state.current_phase == "testing":
        st.subheader("Testing Phase")
        
        if "code_implementation" in st.session_state.artifacts and "user_stories" in st.session_state.artifacts and "design_document" in st.session_state.artifacts:
            code_impl = st.session_state.artifacts["code_implementation"]
            user_stories = st.session_state.artifacts["user_stories"]
            design_doc = st.session_state.artifacts["design_document"]
            
            st.expander("Code Implementation").text_area("Implementation", code_impl, height=200, disabled=True)
            
            if "test_plan" not in st.session_state.artifacts:
                if st.button("Generate Test Plan"):
                    with st.spinner("Generating test plan..."):
                        # Get LLM and agents
                        llm = get_llm()
                        agents = initialize_agents(llm)
                        
                        # Create test plan task
                        test_plan_task = agents["tester"].create_test_plan_task(user_stories, design_doc)
                        
                        # Create and run crew
                        crew = create_crew(
                            agents={"tester": agents["tester"]},
                            tasks=[test_plan_task]
                        )
                        result = crew.kickoff()
                        
                        # Store artifact
                        artifact_id = f"test_plan_{st.session_state.project_id}"
                        db_manager.store_artifact(
                            artifact_id=artifact_id,
                            artifact_content=result,
                            metadata={
                                "type": "test_plan",
                                "project_id": st.session_state.project_id
                            }
                        )
                        
                        # Update session state
                        st.session_state.artifacts["test_plan"] = result
                        
                        st.success("Test plan generated successfully!")
                        st.rerun()
            else:
                test_plan = st.session_state.artifacts["test_plan"]
                st.text_area("Test Plan", test_plan, height=300, disabled=True)
                
                if "test_execution" not in st.session_state.artifacts:
                    if st.button("Execute Tests"):
                        with st.spinner("Executing tests..."):
                            # Get LLM and agents
                            llm = get_llm()
                            agents = initialize_agents(llm)
                            
                            # Create test execution task
                            test_execution_task = agents["tester"].execute_tests_task(test_plan, code_impl)
                            
                            # Create and run crew
                            crew = create_crew(
                                agents={"tester": agents["tester"]},
                                tasks=[test_execution_task]
                            )
                            result = crew.kickoff()
                            
                            # Store artifact
                            artifact_id = f"test_execution_{st.session_state.project_id}"
                            db_manager.store_artifact(
                                artifact_id=artifact_id,
                                artifact_content=result,
                                metadata={
                                    "type": "test_execution",
                                    "project_id": st.session_state.project_id
                                }
                            )
                            
                            # Update session state
                            st.session_state.artifacts["test_execution"] = result
                            
                            st.success("Tests executed successfully!")
                            st.rerun()
                else:
                    test_execution = st.session_state.artifacts["test_execution"]
                    st.text_area("Test Execution Report", test_execution, height=300, disabled=True)
                    
                    if st.button("Proceed to Review Phase"):
                        st.session_state.current_phase = "review"
                        st.rerun()
    
    # Review Phase
    elif st.session_state.current_phase == "review":
        st.subheader("Project Review")
        
        if all(k in st.session_state.artifacts for k in ["project_initialization", "user_stories", "design_document", "code_implementation", "test_plan", "test_execution"]):
            if "project_review" not in st.session_state.artifacts:
                if st.button("Generate Project Review"):
                    with st.spinner("Generating project review..."):
                        # Get LLM and agents
                        llm = get_llm()
                        agents = initialize_agents(llm)
                        
                        # Create status check task
                        artifacts_dict = {k: st.session_state.artifacts[k] for k in st.session_state.artifacts}
                        status_task = agents["project_lead"].create_status_check_task(artifacts_dict)
                        
                        # Create and run crew
                        crew = create_crew(
                            agents={"project_lead": agents["project_lead"]},
                            tasks=[status_task]
                        )
                        result = crew.kickoff()
                        
                        # Store artifact
                        artifact_id = f"project_review_{st.session_state.project_id}"
                        db_manager.store_artifact(
                            artifact_id=artifact_id,
                            artifact_content=result,
                            metadata={
                                "type": "project_review",
                                "project_id": st.session_state.project_id
                            }
                        )
                        
                        # Update session state
                        st.session_state.artifacts["project_review"] = result
                        
                        st.success("Project review generated successfully!")
                        st.rerun()
            else:
                project_review = st.session_state.artifacts["project_review"]
                st.text_area("Project Review", project_review, height=300, disabled=True)
                
                st.success("Project completed successfully!")
                
                if st.button("Start New Project"):
                    # Reset session state
                    st.session_state.project_id = str(uuid.uuid4())
                    st.session_state.artifacts = {}
                    st.session_state.current_phase = "initialization"
                    st.rerun()

#Artifacts Tab
with tab2:
    st.header("Project Artifacts")
    
    # Display artifacts
    for artifact_type, artifact_content in st.session_state.artifacts.items():
        with st.expander(f"{artifact_type.replace('_', ' ').title()}"):
            # Convert CrewOutput to string for display
            content_str = str(artifact_content)
            st.text_area("Content", content_str, height=300, disabled=True, label_visibility="collapsed")
            
            # Download button with string conversion
            st.download_button(
                label=f"Download {artifact_type.replace('_', ' ').title()}",
                data=content_str,
                file_name=f"{artifact_type}_{st.session_state.project_id}.txt",
                mime="text/plain"
            )
# Chat Tab
with tab3:
    st.header(f"Chat with PROJECT MANAGER")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"👤 **Project Manager:** {message['content']}")
        else:
            st.write(f"🤖 **Project Lead:** {message['content']}")

    
    # Chat input
    with st.form("chat_form"):
        user_message = st.text_area("Chat with the Project Lead", height=100)
        submitted = st.form_submit_button("Send")
        
        if submitted and user_message:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            # Generate response
            with st.spinner("Project Lead is responding..."):
                # Get LLM and agents
                llm = get_llm()
                agents = initialize_agents(llm)
                
                current_date = datetime.datetime.now()
                next_business_day = current_date + datetime.timedelta(days=1)
                if next_business_day.weekday() >= 5:  # 5 and 6 are weekend days
                    next_business_day += datetime.timedelta(days=8 - next_business_day.weekday())  # Adjust for weekend

                # Format the date
                formatted_date = next_business_day.strftime("%A, %B %d, %Y at %I:%M %p")

                task = Task(
                description=f"""
                As the Project Lead, respond to the following message from Project Manager:

                "{user_message}"
                
                Current project status:
                - Phase: {st.session_state.current_phase}
                - Artifacts: {', '.join(st.session_state.artifacts.keys()) if st.session_state.artifacts else 'None yet'}
                - Current date: {current_date.strftime("%A, %B %d, %Y")}
                
                Provide a helpful, concise response based on the current project status.
                If you need to reference a future delivery date, use concrete dates instead of placeholders.
                For example, instead of saying "I'll provide a report by [Time/Date]", say "I'll provide a report by {formatted_date}".
                
                Use specific dates and times for any commitments or deadlines you mention.
                """,
                agent=agents["project_lead"].get_agent(),
                expected_output=f"A helpful response to Project Manager with specific dates for any commitments"
            )
                
                # Create and run crew
                crew = create_crew(
                    agents={"project_lead": agents["project_lead"]},
                    tasks=[task]
                )
                result = crew.kickoff()
                
                # Add response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": result})
                
                # Rerun to update chat history
                st.rerun()

# Footer
st.markdown("---")
st.markdown("*made with ❤️ by DeepGen Squad*")