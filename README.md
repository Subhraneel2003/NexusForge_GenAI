# 🤖 NexusForge: Advanced AI Development Framework

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)

## Overview

NexusForge is a comprehensive development framework designed to orchestrate multiple AI agents collaboratively on complex tasks within a unified ecosystem. The system leverages the CrewAI architecture to enable specialized AI agents to work in concert, each contributing unique capabilities to solve multi-faceted development challenges.

By simulating a virtual development pod, NexusForge streamlines the software development lifecycle from project initialization through testing and review, creating an intelligent, collaborative development environment.

## Features

- **Multi-Agent Collaboration**: Orchestrates specialized AI agents working together on software projects
- **Full SDLC Support**: Covers the entire software development lifecycle from requirements to testing
- **Interactive UI**: Built with Streamlit for easy project management and visualization
- **Knowledge Management**: Stores and retrieves project artifacts with ChromaDB
- **Phase-Based Workflow**: Structured approach to software development processes

## Project Architecture

```
NexusForge_GENAI/
├── .env                  # Environment variables
├── app.py                # Streamlit application
├── agents/               # Agent definitions
│   ├── __init__.py       # Base agent class
│   ├── project_lead.py   # Project Lead agent
│   ├── business_analyst.py # Business Analyst agent
│   ├── designer.py       # Designer agent
│   ├── developer.py      # Developer agent
│   └── tester.py         # Tester agent
├── templates/            # Artifact templates
│   ├── user_story.md     # Template for user stories
│   ├── design_doc.md     # Template for design documents
│   ├── code_template.py  # Template for code implementation
│   └── test_case.md      # Template for test cases
├── database/             # ChromaDB setup
│   └── db_manager.py     # Database manager for artifact storage
└── utils/                # Utility functions
    └── helpers.py        # Helper functions for artifact management
```

## Tech Stack

- **Frontend**: Streamlit
- **LLM Integration**: LangChain, LiteLLM
- **Multi-Agent Framework**: CrewAI
- **Database**: ChromaDB (vector database)
- **LLM Models**: Google Gemini 1.5 Flash (configurable)
- **Language**: Python 3.9+

## Agent Ecosystem and Roles

NexusForge implements a virtual development pod with five specialized AI agents:

### 1. Project Lead Agent
- **Role**: Coordinates the development team and project management
- **Tasks**:
  - Project initialization and scope definition
  - Risk assessment and timeline planning
  - Status reporting and milestone tracking
  - Overall project coordination

### 2. Business Analyst Agent
- **Role**: Translates business needs into technical requirements
- **Tasks**: 
  - Creating detailed user stories based on project requirements
  - Refining user stories based on feedback
  - Ensuring requirements are specific, measurable, achievable, relevant, and time-bound

### 3. Designer Agent
- **Role**: Creates comprehensive software design documentation
- **Tasks**:
  - Developing system architecture
  - Creating data models and API designs
  - Determining component interactions and interfaces
  - Addressing non-functional aspects (scalability, security, performance)

### 4. Developer Agent
- **Role**: Implements code based on design specifications
- **Tasks**:
  - Writing clean, maintainable code
  - Implementing functionality specified in user stories
  - Code reviews and refinements
  - Error handling and testing

### 5. Tester Agent
- **Role**: Ensures software quality through comprehensive testing
- **Tasks**:
  - Creating detailed test plans and test cases
  - Executing tests against implemented code
  - Identifying bugs and quality issues
  - Generating test execution reports

## Dataflow and Agent Synchronization

NexusForge implements a sequential workflow where agents collaborate through shared artifacts:

1. **Project Initialization**:
   - User provides requirements (text or PDF)
   - Project Lead agent processes requirements and creates initialization document
   - Initialization document defines scope, epics, and timeline

2. **Requirements Analysis**:
   - Business Analyst agent creates user stories from initialization document
   - User stories are refined based on feedback
   - Final user stories become input for Design phase

3. **Design Phase**:
   - Designer agent creates comprehensive design documentation based on user stories
   - Design document is refined based on feedback
   - Final design becomes input for Development phase

4. **Development Phase**:
   - Developer agent implements code based on user stories and design
   - Code is refined based on feedback
   - Final code implementation becomes input for Testing phase

5. **Testing Phase**:
   - Tester agent creates test plan based on user stories and design
   - Tests are executed against the code implementation
   - Test execution report is generated

6. **Review Phase**:
   - Project Lead agent reviews all artifacts and generates final report
   - Project status and quality assessment is provided

## RAG (Retrieval-Augmented Generation) Scope

The NexusForge framework incorporates RAG capabilities through:

1. **Artifact Storage**: All project artifacts are stored in ChromaDB with metadata
2. **Contextual Generation**: Each new phase uses previous phase artifacts as context
3. **Knowledge Retrieval**: Agents can retrieve relevant artifacts to inform their reasoning
4. **Agent Memory**: Previous decisions and design choices are accessible throughout the project lifecycle

The database manager (`db_manager.py`) handles:
- Storing artifacts with metadata
- Retrieving artifacts by ID or type
- Updating artifacts with new versions
- Supporting project continuity by maintaining a project knowledge base

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Google API key for Gemini model access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/NexusForge_GENAI.git
cd NexusForge_GENAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
```

### Running the Application

```bash
streamlit run app.py
```

## Usage

1. **Start a New Project**: 
   - Enter project details and requirements or upload a PDF
   - Initialize the project to generate a project plan

2. **Generate User Stories**:
   - Review and refine user stories created by the Business Analyst agent

3. **Create Design Document**:
   - Generate a comprehensive design document from the Designer agent
   - Provide feedback to refine the design

4. **Implement Code**:
   - Let the Developer agent create code implementation
   - Review and refine the code as needed

5. **Test the Implementation**:
   - Generate test plans and execute tests against the code
   - Review test results and quality issues

6. **Review the Project**:
   - Get a complete project review and status report

## Future Enhancements

- Integration with version control systems (Git)
- Support for additional LLM models
- CI/CD pipeline generation
- Expanded agent specializations (DevOps, Security, UX/UI)
- Real-time collaborative editing
- Advanced RAG techniques with semantic search

## Advanced Features

### Context-Aware Chat System
- Project Manager queries trigger retrieval of relevant artifacts.
- Project Lead agent provides accurate responses using retrieved context.

### Progressive Knowledge Refinement
- User feedback enhances artifact quality over multiple refinement cycles.

### Cross-Phase Knowledge Transfer
- Ensures consistency across all phases of development by tracing requirements through design, implementation, and testing.


## Challenges Addressed

1. **Context Window Limitations**: Intelligent chunking prioritizes relevant content for large projects.
2. **Knowledge Consistency**: Centralized artifact storage ensures agents work with consistent information.
3. **Retrieval Relevance**: Metadata enrichment optimizes semantic search accuracy.
4. **User Experience Transparency**: Clear UI displays which documents influence current generation.
  

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CrewAI for the multi-agent framework
- LangChain for LLM integration capabilities
- Streamlit for the interactive UI framework
- ChromaDB for vector database
- Google for Gemini model access
