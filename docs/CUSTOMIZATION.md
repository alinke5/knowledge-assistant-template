# 🎨 Customization Guide

This guide shows you how to customize the Knowledge Assistant UI for your specific use case, branding, and requirements.

## 🎯 Basic Customization

### Update App Title and Branding

#### Change the Header
```python
# In app.py, update the display_header() function
def display_header():
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🏢 Your Company Name Knowledge Hub 📚</h1>
        <p class="main-subtitle">Your AI-powered assistant for [your specific domain]</p>
    </div>
    """, unsafe_allow_html=True)
```

#### Update Page Configuration
```python
# In the main() function
st.set_page_config(
    page_title="Your Company Knowledge Hub",
    page_icon="🏢",  # Change to your company logo or relevant emoji
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Customize Example Questions

#### Update Welcome Message
```python
def display_welcome_message():
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-card">
            <h3 style="margin-top: 0; color: #92400e;">👋 Welcome to [Company] Knowledge Assistant!</h3>
            <p style="margin-bottom: 0; color: #451a03;">
                I'm here to help you with [specific domain knowledge]. 
                Ask me about [list your main areas of expertise]!
            </p>
        </div>
        """, unsafe_allow_html=True)
```

#### Add Your Domain-Specific Questions
```python
# Example for HR Knowledge Base
with col1:
    st.markdown("### 👥 HR & Policies")
    example_questions = [
        "What is our remote work policy?",
        "How do I request time off?",
        "What benefits are available?",
        "Who do I contact for HR issues?"
    ]

# Example for Technical Documentation
with col2:
    st.markdown("### 🔧 Technical Support")
    example_questions = [
        "How do I reset my password?",
        "What software is available?",
        "How do I access the VPN?",
        "Who handles IT support tickets?"
    ]

# Example for Legal/Compliance
with col1:
    st.markdown("### ⚖️ Legal & Compliance")
    example_questions = [
        "What is our data privacy policy?",
        "How do we handle contracts?",
        "What are the compliance requirements?",
        "Who reviews legal documents?"
    ]
```

## 🎨 Advanced UI Customization

### Update Color Scheme

#### Change the Gradient Header
```python
# In load_css(), update the header styling
.main-header {
    background: linear-gradient(90deg, #your-primary-color 0%, #your-secondary-color 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
```

#### Common Color Schemes
```css
/* Corporate Blue */
background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);

/* Professional Green */
background: linear-gradient(90deg, #059669 0%, #10b981 100%);

/* Modern Purple */
background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);

/* Executive Gray */
background: linear-gradient(90deg, #374151 0%, #6b7280 100%);
```

### Customize Stats Cards

#### Update Stats for Your Domain
```python
def display_stats():
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">📚</div>
            <div class="stat-label">Policy Expert</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">⚡</div>
            <div class="stat-label">Instant Answers</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">🔒</div>
            <div class="stat-label">Secure & Private</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">✅</div>
            <div class="stat-label">Always Current</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

### Update Sidebar Content

#### Customize Sidebar Information
```python
# In the sidebar section
with st.sidebar:
    st.markdown("### 📊 Session Info")
    st.markdown(f"**User:** {user_info.get('user_name', 'Guest')}")
    st.markdown(f"**Department:** HR")  # Add department if available
    st.markdown(f"**Time:** {datetime.now().strftime('%I:%M %p')}")
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")
    
    st.markdown("---")
    st.markdown("### 🎯 I Can Help With")
    st.markdown("""
    - **Company Policies**
    - **HR Procedures**  
    - **Benefits Information**
    - **Contact Directory**
    - **Process Guidelines**
    - **Document Search**
    """)
    
    st.markdown("---")
    st.markdown("### 📞 Need More Help?")
    st.markdown("""
    **HR Team**: hr@company.com  
    **IT Support**: it@company.com  
    **Phone**: (555) 123-4567
    """)
```

## 🔧 Functional Customization

### Update Chat Input Placeholder
```python
prompt = st.chat_input("Ask me about company policies, procedures, or benefits... 📋", key="main_chat_input")
```

### Customize Error Messages
```python
# Update error handling for your domain
if "authentication" in error_msg.lower():
    st.error("🔐 Authentication issue with the company knowledge base.")
    st.info("📞 Please contact IT support for access issues.")
elif "validation" in error_msg.lower():
    st.error("🔧 Question format issue.")
    st.info("💡 **Try rephrasing your question**, such as:\n- 'What is the policy on...'\n- 'How do I process...'")
```

### Add Custom Loading Messages
```python
with st.spinner("Searching company knowledge base..."):
    # or
with st.spinner("Looking through HR policies..."):
    # or
with st.spinner("Checking technical documentation..."):
```

## 🏢 Industry-Specific Templates

### Healthcare Organization
```python
# Header
<h1 class="main-title">🏥 MedCorp Policy Assistant 💊</h1>
<p class="main-subtitle">Your AI guide for healthcare policies and procedures</p>

# Example questions
example_questions = [
    "What is our patient privacy policy?",
    "How do I report a safety incident?",
    "What are the infection control procedures?",
    "Who do I contact for medical emergencies?"
]

# Stats
<div class="stat-number">🏥</div>
<div class="stat-label">Healthcare Expert</div>
```

### Financial Services
```python
# Header
<h1 class="main-title">🏦 FinCorp Compliance Assistant 💰</h1>
<p class="main-subtitle">Your AI guide for financial regulations and policies</p>

# Example questions
example_questions = [
    "What are the KYC requirements?",
    "How do I handle suspicious transactions?",
    "What is our risk management policy?",
    "Who reviews compliance issues?"
]
```

### Technology Company
```python
# Header
<h1 class="main-title">💻 TechCorp Knowledge Hub 🚀</h1>
<p class="main-subtitle">Your AI assistant for engineering and product documentation</p>

# Example questions
example_questions = [
    "How do I deploy to production?",
    "What is our code review process?",
    "How do I access the development environment?",
    "What are our security guidelines?"
]
```

### Educational Institution
```python
# Header
<h1 class="main-title">🎓 University Policy Assistant 📚</h1>
<p class="main-subtitle">Your AI guide for academic policies and procedures</p>

# Example questions
example_questions = [
    "What is the grade appeal process?",
    "How do I register for classes?",
    "What are the graduation requirements?",
    "Who do I contact for academic advising?"
]
```

## 📱 Mobile Optimization

### Responsive Design Updates
```css
/* Add to load_css() function */
@media (max-width: 768px) {
    .main-title {
        font-size: 1.8rem;
    }
    
    .stats-container {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .stat-card {
        padding: 1rem;
    }
}
```

## 🔒 Security Customization

### Add Disclaimer
```python
# Add to sidebar or footer
st.markdown("---")
st.markdown("### ⚠️ Important Notice")
st.markdown("""
This assistant provides information based on company documentation. 
For official decisions or sensitive matters, please consult with 
the appropriate department directly.
""")
```

## 📊 Analytics Integration

### Add Usage Tracking
```python
# Add to handle_chat_interaction()
import uuid

# Track user interactions
def log_interaction(question, response):
    interaction_id = str(uuid.uuid4())
    # Log to your analytics platform
    print(f"Interaction {interaction_id}: {question[:50]}...")
```

## 🎯 Performance Optimization

### Optimize for Speed
```python
# Reduce max_tokens for faster responses
assistant_response = query_endpoint(
    endpoint_name=SERVING_ENDPOINT,
    messages=st.session_state.messages,
    max_tokens=256,  # Adjust based on your needs
)["content"]
```

### Cache Frequently Asked Questions
```python
# Add caching for common questions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_response(question):
    # Check if this is a frequently asked question
    faq_responses = {
        "what is the remote work policy": "Our remote work policy allows...",
        # Add more FAQs
    }
    return faq_responses.get(question.lower())
```

## 🚀 Deployment Variations

### Development vs Production
```python
# Add environment detection
import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'development':
    # Show debug information
    st.sidebar.markdown("### 🛠️ Debug Info")
    st.sidebar.json({"endpoint": SERVING_ENDPOINT, "env": ENVIRONMENT})
```

Remember to test all customizations thoroughly before deploying to production! 🧪
