import logging
import os
import streamlit as st
from model_serving_utils import query_endpoint, is_endpoint_supported
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure environment variable is set correctly
SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
assert SERVING_ENDPOINT, \
    ("Unable to determine serving endpoint to use for chatbot app. If developing locally, "
     "set the SERVING_ENDPOINT environment variable to the name of your serving endpoint. If "
     "deploying to a Databricks app, include a serving endpoint resource named "
     "'serving_endpoint' with CAN_QUERY permissions, as described in "
     "https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app#deploy-the-databricks-app")

# Check if the endpoint is supported
endpoint_supported = is_endpoint_supported(SERVING_ENDPOINT)

def get_user_info():
    headers = st.context.headers
    return dict(
        user_name=headers.get("X-Forwarded-Preferred-Username"),
        user_email=headers.get("X-Forwarded-Email"),
        user_id=headers.get("X-Forwarded-User"),
    )

# Custom CSS for professional styling
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #059669 50%, #dc2626 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        background: rgba(255,255,255,0.95);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Chat Messages */
    .stChatMessage {
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* User Message */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
    }
    
    /* Assistant Message */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
    }
    
    /* Input Styling */
    .stChatInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        background: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #bfdbfe;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin: 0;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Sidebar Styling */
    .sidebar-content {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #2563eb;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🏢 Knowledge Assistant 📚</h1>
        <p class="main-subtitle">Your AI-powered expert for company knowledge and documentation</p>
    </div>
    """, unsafe_allow_html=True)

def display_welcome_message():
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-card">
            <h3 style="margin-top: 0; color: #92400e;">👋 Welcome to the Knowledge Assistant!</h3>
            <p style="margin-bottom: 0; color: #451a03;">
                I'm here to help you find information from your company's knowledge base. 
                Ask me anything about policies, procedures, guidelines, or any documents in our system!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Example questions - CUSTOMIZE THESE FOR YOUR USE CASE
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Policy Examples")
            example_questions = [
                "What is the remote work policy?",
                "How do I request time off?",
                "What are the employee benefits?",
                "Where can I find the employee handbook?"
            ]
            for q in example_questions:
                if st.button(q, key=f"policy_{q[:10]}", use_container_width=True):
                    st.session_state.selected_question = q
                    st.rerun()
        
        with col2:
            st.markdown("### 📖 General Examples")
            example_questions = [
                "How do I onboard a new employee?",
                "What are the security guidelines?",
                "Who do I contact for IT support?",
                "What is the expense reimbursement process?"
            ]
            for q in example_questions:
                if st.button(q, key=f"general_{q[:10]}", use_container_width=True):
                    st.session_state.selected_question = q
                    st.rerun()

def display_stats():
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">📚</div>
            <div class="stat-label">Knowledge Expert</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">🔍</div>
            <div class="stat-label">Document Search</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Always Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">🤖</div>
            <div class="stat-label">AI-Powered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_chat_interaction():
    # Handle pre-selected questions
    if "selected_question" in st.session_state:
        prompt = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        prompt = st.chat_input("Ask me about company policies, procedures, or any documentation... 📚", key="main_chat_input")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with loading state
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                try:
                    # Query the Databricks serving endpoint
                    assistant_response = query_endpoint(
                        endpoint_name=SERVING_ENDPOINT,
                        messages=st.session_state.messages,
                        max_tokens=512,  # Reduced for better response times
                    )["content"]
                    
                    # Display response with typing effect
                    st.markdown(assistant_response)
                    
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Error querying endpoint: {e}")
                    
                    if "authentication" in error_msg.lower() or "token" in error_msg.lower():
                        st.error("🔐 Authentication issue with the knowledge base.")
                        st.info("📞 Please contact your administrator to check endpoint permissions.")
                    elif "validation" in error_msg.lower() or "schema" in error_msg.lower():
                        st.error("🔧 Data format issue when querying the knowledge base.")
                        st.info("💡 **Try asking your question in a different way**, such as:\n- 'Explain the remote work policy'\n- 'What is the process for expense reimbursement?'")
                    elif "failed" in error_msg.lower() and "approaches" in error_msg.lower():
                        st.error("⚠️ Multiple connection attempts to the knowledge base failed.")
                        st.info(f"🔍 **Technical details:** {error_msg[:200]}...")
                        st.info("🔄 Please try again in a moment, or contact support if the issue persists.")
                    else:
                        st.error("⚠️ I'm experiencing technical difficulties connecting to the knowledge base.")
                        st.info("🔄 Please try again in a moment, or try asking a different question.")
                    
                    assistant_response = "I apologize for the technical issue. Please try rephrasing your question or try one of the example questions above."

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

def main():
    # Page configuration
    st.set_page_config(
        page_title="Knowledge Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Check user info
    user_info = get_user_info()
    
    # Main layout
    display_header()
    
    # Check if endpoint is supported
    if not endpoint_supported:
        st.error("⚠️ **Service Temporarily Unavailable**")
        st.markdown(
            f"""
            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                <p><strong>Technical Issue:</strong> The knowledge assistant endpoint is currently not accessible.</p>
                <p>Please contact your administrator or try again later.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 📊 Session Info")
        st.markdown(f"**User:** {user_info.get('user_name', 'Guest')}")
        st.markdown(f"**Time:** {datetime.now().strftime('%I:%M %p')}")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        
        st.markdown("---")
        st.markdown("### 🎯 What I Can Help With")
        st.markdown("""
        - **Company Policies & Procedures**
        - **Employee Guidelines**  
        - **Documentation Search**
        - **Process Instructions**
        - **Contact Information**
        - **Official Interpretations**
        """)
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    with st.container():
        # Welcome message and examples
        display_welcome_message()
        
        # Stats display
        if len(st.session_state.messages) == 0:
            display_stats()
        
        # Chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat interaction
        handle_chat_interaction()

if __name__ == "__main__":
    main()
