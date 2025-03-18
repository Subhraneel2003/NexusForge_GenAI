# 🤖 NexusForge: Advanced AI Development Framework

## Overview

NexusForge is a Streamlit application that simulates a complete software development team using AI agents. Each agent specializes in a different role of the software development lifecycle, allowing you to rapidly prototype and develop software projects with minimal human intervention.

## Features

- **Complete Development Lifecycle**: Takes projects from initial requirements through design, development, testing, and review phases
- **Specialized AI Agents**: Utilizes AI agents for different roles including Project Lead, Business Analyst, Designer, Developer, and Tester
- **Interactive Interface**: Streamlit-based UI that allows for real-time interaction and feedback at each development phase
- **Artifact Management**: Automatically generates and manages development artifacts throughout the project lifecycle
- **Chat Interface**: Direct communication with the Project Lead agent for questions and guidance

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-development-pod.git
   cd ai-virtual-development-pod
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. The application will open in your default web browser at `http://localhost:8501`

3. Navigate through the different tabs and phases of development:
   - **Project Management**: Guide the project through each development phase
   - **Artifacts**: View and download generated project artifacts
   - **Chat**: Communicate directly with the Project Lead agent

## Development Workflow

1. **Initialization Phase**:
   - Enter project name, description, and business requirements
   - The Project Lead agent will generate an initial project outline

2. **Requirements Analysis Phase**:
   - The Business Analyst agent generates user stories based on the project outline
   - Provide feedback to refine the user stories as needed

3. **Design Phase**:
   - The Designer agent creates a comprehensive design document
   - Review and provide feedback to refine the design

4. **Development Phase**:
   - The Developer agent generates code implementation based on design and requirements
   - Review and provide feedback to improve the code

5. **Testing Phase**:
   - The Tester agent creates a test plan and executes tests against the implementation
   - Review test results and address any issues

6. **Review Phase**:
   - The Project Lead agent provides a comprehensive project review
   - Start a new project or continue refining the current one

## Project Structure

```
virtual_dev_pod/
├── .env                  # Environment variables
├── app.py                # Streamlit application
├── agents/               # Agent definitions
│   ├── __init__.py
│   ├── project_lead.py
│   ├── business_analyst.py
│   ├── designer.py
│   ├── developer.py
│   └── tester.py
├── templates/            # Artifact templates
│   ├── user_story.md
│   ├── design_doc.md
│   ├── code_template.py
│   └── test_case.md
├── database/             # ChromaDB setup
│   └── db_manager.py
└── utils/                # Utility functions
    └── helpers.py
```

## Customization

### Adding New Agents

To add a new specialized agent:

1. Create a new file in the `agents/` directory
2. Define the agent class with appropriate methods
3. Update the imports and agent initialization in `app.py`

### Modifying the Workflow

You can customize the development workflow by:

1. Adding or removing phases in the sidebar selection
2. Modifying the tasks given to agents
3. Creating new artifact types

## Troubleshooting

- **API Key Issues**: Ensure your API keys are correctly set in the `.env` file
- **Memory Errors**: If you encounter memory issues with large projects, try reducing the model's temperature or tokens
- **Missing Task Import**: If you encounter a "Task not defined" error, ensure you've imported `Task` from the crewai package

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI agents powered by [CrewAI](https://github.com/joaomdmoura/crewai)
- Language models provided by Google's Gemini API
