# 🏈⚾ Sports Rules Knowledge Assistant - Public Template

A professional Streamlit chatbot built with **Databricks Agent Bricks Knowledge Assistant** for answering questions about sports rules with citations. This template can be adapted for any knowledge base - HR policies, technical documentation, legal contracts, and more!

![Sports Rules Assistant](https://img.shields.io/badge/Databricks-Agent%20Bricks-red) ![Streamlit](https://img.shields.io/badge/Streamlit-App-green) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🌟 Features

- **🤖 AI-Powered Knowledge Assistant** using Databricks Agent Bricks
- **🎨 Professional Sports-Themed UI** with modern design
- **💬 Interactive Chat Interface** with example questions
- **📱 Responsive Design** for desktop and mobile
- **🔄 Direct Databricks Sync** for seamless deployment
- **📊 Session Management** and chat history
- **🎯 Professional Error Handling** with user-friendly messages

## 🚀 Quick Start

### Prerequisites

1. **Databricks Workspace** with:
   - Agent Bricks enabled
   - Unity Catalog enabled
   - Serverless compute enabled
   - Model Serving access

2. **Databricks CLI** installed and configured

### Step 1: Create Your Knowledge Assistant

1. **Upload Your Documents**
   ```bash
   # Upload your PDFs/documents to Unity Catalog volume
   # Example: /Volumes/main/default/sports_rules/
   ```

2. **Create Agent Bricks Knowledge Assistant**
   - Go to **Agents** in Databricks workspace
   - Click **Knowledge Assistant**
   - Configure with your document volume
   - Note your endpoint name (e.g., `your-endpoint-name`)

### Step 2: Clone and Configure

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/sports-rules-assistant
   cd sports-rules-assistant
   ```

2. **Update configuration**
   - Edit `app.yaml` with your endpoint name
   - Update `databricks.yml` with your endpoint details
   - Customize the UI theme in `app.py`

### Step 3: Deploy to Databricks

1. **Sync to Databricks**
   ```bash
   databricks sync . /Workspace/Users/your.email@company.com/your-app-name
   ```

2. **Deploy using Databricks Apps**
   - Navigate to your workspace
   - Deploy through Databricks Apps interface

## 📁 Repository Structure

```
├── app.py                    # Main Streamlit application
├── app.yaml                  # Databricks App configuration
├── databricks.yml            # Resource configuration
├── model_serving_utils.py    # Endpoint integration utilities
├── requirements.txt          # Python dependencies
├── debug_app.py             # Debug/testing interface
├── test_endpoint.py         # Endpoint testing script
├── README.md                # This file
└── docs/
    ├── SETUP_GUIDE.md       # Detailed setup instructions
    ├── CUSTOMIZATION.md     # UI customization guide
    └── TROUBLESHOOTING.md   # Common issues and solutions
```

## 🎨 Customization

### Update Branding
```python
# In app.py, update the header and theme
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏢 Your Company Knowledge Assistant 📚</h1>
    <p class="main-subtitle">Your AI-powered expert for company policies and procedures</p>
</div>
""", unsafe_allow_html=True)
```

### Add Your Example Questions
```python
# In app.py, update example questions
example_questions = [
    "What is our remote work policy?",
    "How do I request time off?",
    "What are the benefits enrollment deadlines?",
    "Where can I find the employee handbook?"
]
```

### Update Colors and Styling
```css
/* In app.py load_css() function */
.main-header {
    background: linear-gradient(90deg, #your-color1 0%, #your-color2 100%);
}
```

## 📋 Configuration Files

### app.yaml
```yaml
command: [
  "streamlit", 
  "run",
  "app.py"
]

env:
  - name: STREAMLIT_BROWSER_GATHER_USAGE_STATS
    value: "false"
  - name: "SERVING_ENDPOINT"
    valueFrom: "serving-endpoint"
```

### databricks.yml
```yaml
resources:
  serving-endpoints:
    serving-endpoint:
      name: "YOUR_ENDPOINT_NAME"  # Replace with your endpoint
      permissions:
        - level: CAN_QUERY
          principal: "{{workspace.current_user.userName}}"
```

## 🔧 Use Cases

This template can be adapted for:

- **📋 HR Knowledge Base** - Employee policies, benefits, procedures
- **⚖️ Legal Document Assistant** - Contract Q&A, compliance guidance
- **📖 Technical Documentation** - API docs, user manuals, troubleshooting
- **🎓 Training Materials** - Course content, certification guides
- **🏥 Healthcare Protocols** - Medical guidelines, procedure manuals
- **🏭 Operations Manuals** - Safety procedures, equipment guides

## 🆘 Support

- **Setup Issues**: See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
- **Customization**: See [CUSTOMIZATION.md](docs/CUSTOMIZATION.md)
- **Troubleshooting**: See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Databricks Docs**: [Agent Bricks Knowledge Assistant](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/knowledge-assistant)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Databricks** for the incredible Agent Bricks platform
- **Streamlit** for the beautiful UI framework
- **Cursor** for making development a breeze
- **The Community** for inspiration and feedback

---

**Built with ❤️ using Databricks Agent Bricks and Streamlit**

*Transform your documents into intelligent assistants in minutes, not months!*
