# Code Analyzer Agentic AI

An AI-powered **Code Analyzer Chatbot** built with **Streamlit, LangGraph, LangChain, and Groq**. The application accepts a code snippet from the user and uses an LLM-based agent to analyze the code, identify possible issues, and suggest improvements.

## Project Overview

The Code Analyzer Agentic AI application provides an interactive interface where users can paste a code snippet and request an AI-based analysis.

The application:

* Accepts code snippets through a Streamlit interface
* Creates a structured analysis prompt
* Uses LangGraph to manage the workflow
* Uses a LangChain agent for LLM interaction
* Uses Groq's `ChatGroq` integration with the `openai/gpt-oss-20b` model
* Provides code analysis guidance through a custom tool
* Identifies potential syntax and logic issues
* Suggests improvements and optimizations
* Considers readability and coding best practices
* Maintains conversation history during the Streamlit session
* Displays the context used for the analysis

## Technologies Used

| Technology           | Purpose                                |
| -------------------- | -------------------------------------- |
| Python               | Application development                |
| Streamlit            | Web interface                          |
| LangChain            | LLM and agent framework                |
| LangGraph            | Workflow and state management          |
| Groq                 | LLM inference                          |
| `openai/gpt-oss-20b` | Language model used by the application |

## Architecture

The application follows a simple LangGraph workflow:

```text
User
  |
  v
Paste Code in Streamlit
  |
  v
Create Prompt Node
  |
  |-- Analyze Code Context
  |
  v
Generate Response Node
  |
  |-- LangChain Agent
  |       |
  |       v
  |   Groq LLM
  |
  v
AI Code Analysis
  |
  v
Display Result
  |
  v
Conversation History
```

## LangGraph Workflow

The application defines a `CodeState` state schema containing:

```text
query
context
messages
response
```

The workflow contains two main nodes:

### 1. `create_prompt`

This node:

* Receives the user's code
* Creates context for the code
* Builds a structured prompt
* Stores the prompt as a `HumanMessage`

### 2. `generate_response`

This node:

* Retrieves the cached LangChain agent
* Sends the prompt to the agent
* Receives the AI response
* Stores the response in the application state

The graph is defined as:

```text
START
  |
  v
create_prompt
  |
  v
generate_response
  |
  v
END
```

## Agent Tool

The application defines a custom LangChain tool:

```python
@tool
def get_code_analysis_guidance(query: str) -> str:
```

The tool provides the agent with general code-analysis guidance focusing on:

* Syntax errors
* Logic errors
* Performance
* Readability
* Best practices

## Streamlit Interface

The application provides:

### Code Input

Users can paste their code into a text area and click **Analyze**.

### Analysis Result

The application displays:

* The submitted code
* AI-generated analysis
* Context used during analysis

### Conversation History

Previous analyses are stored in Streamlit session state and displayed in expandable sections.

## Project Structure

```text
Code_Analyser_Agentic_AI/
│
├── code_analyser_chatbot.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/poreddyrithika/Code_Analyser_Agentic_AI.git
```

### 2. Navigate to the Project

```bash
cd Code_Analyser_Agentic_AI
```

### 3. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## API Key Configuration

The application requires a **Groq API key**.

Do not hard-code your API key in the Python source code or commit it to GitHub.

### Recommended Setup

Change the API-key section of the Python file to:

```python
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not set. Please configure it as an environment variable.")
    st.stop()
```

Then set the environment variable.

### Windows PowerShell

For the current terminal session:

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

Alternatively, create a `.env` file locally:

```text
GROQ_API_KEY=your_groq_api_key
```

Make sure `.env` is included in `.gitignore`.

## Running the Application

After installing the dependencies and configuring the API key, run:

```powershell
streamlit run code_analyser_chatbot.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

## How to Use

1. Start the Streamlit application.
2. Paste a code snippet into the text area.
3. Click **Analyze**.
4. The application sends the code through the LangGraph workflow.
5. The AI agent analyzes the code.
6. The generated analysis is displayed.
7. Previous analyses are available under **Conversation History**.

## Example

Input:

```python
def add(a, b)
    return a + b
```

The analyzer can identify issues such as:

* Missing colon after the function definition
* Possible syntax error
* Suggested corrected code

## Key Features

### AI Code Analysis

Analyzes submitted code using an LLM-based agent.

### Agent-Based Architecture

Uses LangChain's agent framework to process the analysis request.

### LangGraph Workflow

Uses a state-based graph to organize the prompt creation and response generation stages.

### Custom Tool

Provides code-analysis guidance to the agent through a custom LangChain tool.

### Session-Based Conversation History

Uses Streamlit session state to maintain previous analyses during the current application session.

### Context Display

Allows users to view the context generated for their submitted code.

### Error Handling

The application uses exception handling around the analysis workflow.

If an error occurs, Streamlit displays:

*The error message

*The Python traceback

This helps during development and debugging.
