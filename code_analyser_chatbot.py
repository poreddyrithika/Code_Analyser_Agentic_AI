import os
import streamlit as st
from typing import TypedDict, Annotated
from operator import add
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain.agents import create_agent
# Set your GROQ API Key
api_key = "GROQ_API_KEY"
if not api_key:
    st.error("GROQ_API_KEY not set. Please configure it as an environment variable.")
    st.stop()
# Setup LLM
llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-20b",
    api_key=api_key,
)
# State Schema
class CodeState(TypedDict):
    query: str
    context: str
    messages: Annotated[list, add]
    response: str
# Helper Functions
def analyze_code_context(query: str) -> str:
    """Analyze code and provide context."""
    return f"Analyzing the following code snippet:\n{query}"
# Define Tools for the Agent
@tool
def get_code_analysis_guidance(query: str) -> str:
    """Get guidance on how to analyze code properly."""
    return (
        "Focus on: syntax errors, logic errors, performance, "
        "readability, and best practices."
    )
tools = [get_code_analysis_guidance]
# Build the Agent Once (cached)
@st.cache_resource
def get_agent():
    return create_agent(
        model=llm,
        tools=tools
    )
# LangGraph Nodes
def create_prompt_node(state: CodeState) -> CodeState:
    """Create a structured prompt with code snippet."""
    query = state["query"]
    context = analyze_code_context(query)
    prompt = f"""
You are a code analysis assistant.
Context:
{context}

Task:
- Analyze the code snippet
- Identify potential issues or bugs
- Suggest improvements or optimizations
- Explain your reasoning step by step

User Code:
{query}
"""
    return {
        **state,
        "context": context,
        "messages": [
            HumanMessage(content=prompt)
        ]
    }
def generate_response_node(state: CodeState) -> CodeState:
    """Generate response using LLM."""
    agent = get_agent()
    response = agent.invoke(
        {
            "messages": state["messages"]
        }
    )
    if response and "messages" in response:
        bot_message = response["messages"][-1]
        response_text = bot_message.content
    else:
        response_text = str(response)
    return {
        **state,
        "response": response_text,
        "messages": state["messages"] + [
            AIMessage(content=response_text)
        ]
    }
# Build LangGraph Workflow
def build_code_graph():
    graph = StateGraph(CodeState)
    graph.add_node(
        "create_prompt",
        create_prompt_node
    )
    graph.add_node(
        "generate_response",
        generate_response_node
    )
    graph.add_edge(
        START,
        "create_prompt"
    )
    graph.add_edge(
        "create_prompt",
        "generate_response"
    )
    graph.add_edge(
        "generate_response",
        END
    )
    return graph.compile()
code_workflow = build_code_graph()
# Streamlit UI
st.title("Code Analyzer Chatbot (LangGraph + LLM)")
# Initialize Session State
if "conversation" not in st.session_state:
    st.session_state.conversation = []
# Input Form for Code
with st.form("code_form"):
    user_code = st.text_area("Paste your code snippet here:")
    submitted = st.form_submit_button("Analyze")
if submitted and user_code and user_code.strip():
    try:
        with st.spinner("Analyzing code..."):
            initial_state = {
                "query": user_code,
                "context": "",
                "messages": [],
                "response": ""
            }
            result = code_workflow.invoke(
                initial_state
            )
        bot_response_text = result.get(
            "response",
            "No response generated"
        )
        st.session_state.conversation.append(
            {
                "user": user_code,
                "bot": bot_response_text
            }
        )
        st.success("Analysis Complete")
        # Display Current Analysis
        st.markdown(
            f"""
**You:**

```python
{user_code}
```
"""
        )
        st.markdown(
            f"""
**Assistant Analysis:**

{bot_response_text}
"""
        )
        # Display Context
        with st.expander("Context Used"):
            st.text(
                result.get(
                    "context",
                    "No context found"
                )
            )
    except Exception as e:
        st.error(
            f"Error: {str(e)}"
        )
        import traceback
        st.error(
            traceback.format_exc()
        )
elif submitted and not (user_code and user_code.strip()):
    st.warning("Please paste some code before clicking Analyze.")
# Display Conversation History
if st.session_state.conversation:
    st.divider()
    st.subheader("Conversation History")
    for i, turn in enumerate(st.session_state.conversation):
        preview_lines = turn['user'].strip().splitlines()[:2]
        preview_text = "\n".join(preview_lines)
        if len(turn['user'].strip().splitlines()) > 2:
            preview_text += " ..."
        with st.expander(preview_text or "Empty code"):
            st.markdown(
                f"""
**You:**

```python
{turn['user']}
```
"""
            )
            st.markdown(
                f"""
**Assistant Analysis:**

{turn['bot']}
"""
            )
