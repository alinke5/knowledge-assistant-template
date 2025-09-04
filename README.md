# 🏈⚾ NFL & MLB Rules Assistant (Public Template)

**Transform your documents into intelligent AI assistants in minutes!** This is the actual, production-ready NFL & MLB rules assistant built with **Databricks Agent Bricks**. Use it as-is for sports rules, or easily adapt it for your own knowledge base - HR policies, technical documentation, legal contracts, and more!

![Databricks](https://img.shields.io/badge/Databricks-Agent%20Bricks-red) ![Streamlit](https://img.shields.io/badge/Streamlit-App-green) ![License](https://img.shields.io/badge/License-MIT-blue) ![Python](https://img.shields.io/badge/Python-3.8+-yellow) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🌟 What You Get

This is an **actual working implementation** of a professional sports rules assistant! You can:

### 🏈⚾ **Use As-Is for Sports Rules**
- Deploy the exact same NFL & MLB rules assistant
- Professional sports-themed UI with modern design
- Official NFL and MLB rulebook integration (you'll need to download these as PDF, & upload to a UC volume - more on that below)
- Ready-to-use example questions and branding

### 🏢 **Adapt for Your Organization**
- Replace sports data with your company documents
- Customize branding for your industry
- Use for HR policies, technical docs, legal contracts, training materials
- Keep the professional UI and user experience

## 🎯 Live Demo Data Sources

This implementation uses **official sports rulebooks**:
- **NFL Official Rulebook**: https://operations.nfl.com/the-rules/nfl-rulebook/
- **MLB Official Rules**: https://mktg.mlbstatic.com/mlb/official-information/2025-official-baseball-rules.pdf

*Download these PDFs and upload to your Unity Catalog volume to recreate the exact same assistant!*

## ✨ Key Features

- **🤖 Agent Bricks Integration** - Seamless knowledge base setup
- **🎨 Professional Sports UI** - Customer-ready appearance
- **💬 Interactive Chat** with domain-specific examples
- **📱 Responsive Design** for desktop 
- **🔄 Direct Databricks Sync** for seamless deployment
- **📊 Session Management** and error handling
- **🎯 Citation Support** - Responses include source references

## 🚀 Quick Start Options

### Option A: Sports Rules Assistant (Use As-Is)

1. **Download Official Rulebooks**
   ```bash
   # Download these files to your local machine:
   # NFL: https://operations.nfl.com/the-rules/nfl-rulebook/
   # MLB: https://mktg.mlbstatic.com/mlb/official-information/2025-official-baseball-rules.pdf
   ```

2. **Upload to Unity Catalog**
   ```sql
   -- Create volume for sports rules
   CREATE VOLUME IF NOT EXISTS main.default.sports_rules;
   
   -- Upload the PDFs through Databricks UI to:
   -- /Volumes/main/default/sports_rules/nfl_rulebook.pdf
   -- /Volumes/main/default/sports_rules/mlb_official_rules.pdf
   ```

3. **Create Agent Bricks Knowledge Assistant**
   - Go to **Agents** → **Knowledge Assistant** in Databricks
   - Name: "NFL-MLB Rules Assistant"
   - Knowledge Source: `/Volumes/main/default/sports_rules/` or whereever you saved the NFL/MLB rules documents
   - Instructions: "Expert on NFL and MLB rules with accurate citations"

### Option B: Adapt for Your Organization (if you want to customize with your own internal company docs)

1. **Replace Data Sources**
   ```sql
   -- Create volume for your documents
   CREATE VOLUME IF NOT EXISTS main.default.company_docs;
   
   -- Upload your PDFs (HR policies, technical docs, etc.)
   -- /Volumes/main/default/company_docs/employee_handbook.pdf
   -- /Volumes/main/default/company_docs/technical_guide.pdf
   ```

2. **Customize the UI**
   ```python
   # In app.py, update the header:
   st.markdown("""
   <div class="main-header">
       <h1 class="main-title">🏢 Your Company Knowledge Assistant 📚</h1>
       <p class="main-subtitle">AI-powered expert for company policies and procedures</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Update example questions:
   example_questions = [
       "What is our remote work policy?",
       "How do I request time off?",
       "What are the IT security guidelines?",
       "Where can I find the employee handbook?"
   ]
   ```

## 📋 Prerequisites

- **Databricks Workspace** with:
  - Agent Bricks enabled (Beta)
  - Unity Catalog enabled
  - Serverless compute enabled
  - Model Serving access
- **Databricks CLI** installed and configured

## 🛠️ Setup Instructions

### 1. Clone This Repository
```bash
git clone https://github.com/alinke5/knowledge-assistant-template
cd knowledge-assistant-template
```

### 2. Configure Your Endpoint
```yaml
# In databricks.yml, replace with your endpoint name:
resources:
  serving-endpoints:
    serving-endpoint:
      name: "YOUR_AGENT_ENDPOINT_NAME"  # Replace this
      permissions:
        - level: CAN_QUERY
          principal: "{{workspace.current_user.userName}}"
```

### 3. Deploy to Databricks
```bash
# Sync to your workspace (if using an IDE). If not, you can import all of the application files into your workspace
databricks sync . /Workspace/Users/your.email@company.com/your-app-name

# Deploy through Databricks Apps UI - this is a manual step!! You need to do this in order for your Databricks app to actually deploy! Select the proper path where your application files live, deploy, and Databricks will stand up the application for you with a clickable link! 

```

## 🎨 Customization Examples

### Healthcare Organization
```python
# Header customization
<h1 class="main-title">🏥 MedCorp Policy Assistant 💊</h1>
<p class="main-subtitle">AI guide for healthcare policies and procedures</p>

# Example questions
example_questions = [
    "What is our patient privacy policy?",
    "How do I report a safety incident?",
    "What are the infection control procedures?",
    "Who do I contact for medical emergencies?"
]
```

### Technology Company
```python
# Header customization
<h1 class="main-title">💻 TechCorp Knowledge Hub 🚀</h1>
<p class="main-subtitle">AI assistant for engineering and product documentation</p>

# Example questions
example_questions = [
    "How do I deploy to production?",
    "What is our code review process?",
    "How do I access the development environment?",
    "What are our security guidelines?"
]
```

### Financial Services
```python
# Header customization
<h1 class="main-title">🏦 FinCorp Compliance Assistant 💰</h1>
<p class="main-subtitle">AI guide for financial regulations and policies</p>

# Example questions
example_questions = [
    "What are the KYC requirements?",
    "How do I handle suspicious transactions?",
    "What is our risk management policy?",
    "Who reviews compliance issues?"
]
```

## 📁 Repository Structure - all of these are required to run the application!!

```
├── app.py                    # Main Streamlit app (NFL/MLB themed)
├── app.yaml                  # Databricks App configuration  
├── databricks.yml            # Resource configuration (sanitized)
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

## 🎯 Use Cases & Industries

### 📋 **Human Resources**
- Employee handbooks and policies
- Benefits and compensation guides
- Onboarding and training materials
- HR process documentation

### ⚖️ **Legal & Compliance**
- Contract templates and analysis
- Regulatory compliance guides
- Legal process documentation
- Policy interpretation assistance

### 🔧 **Technical Documentation**
- API documentation and guides
- System administration manuals
- Troubleshooting knowledge bases
- Software user guides

### 🎓 **Education & Training**
- Course materials and syllabi
- Certification study guides
- Institutional policy manuals
- Training program documentation

### 🏥 **Healthcare**
- Medical procedure guidelines
- Patient care protocols
- Safety and compliance manuals
- Healthcare policy documentation

## 🆘 Support & Documentation

- **📖 Setup Guide**: [Complete setup instructions](docs/SETUP_GUIDE.md)
- **🎨 Customization**: [Branding and UI customization](docs/CUSTOMIZATION.md)  
- **🔧 Troubleshooting**: [Common issues and solutions](docs/TROUBLESHOOTING.md)
- **📚 Databricks Docs**: [Agent Bricks Knowledge Assistant](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/knowledge-assistant)

## 🌟 Why This Template Works

### **Real Implementation** 
This isn't just a demo - it's a production-ready application currently handling sports rules queries with professional-grade UI and error handling.

### **Proven Architecture**
Built using Databricks best practices with proper resource management, security, and scalability considerations.

### **Professional Appearance**
Customer-ready UI suitable for client demonstrations, with modern design and smooth user experience.

### **Comprehensive Documentation**
Everything you need to deploy, customize, and maintain your knowledge assistant.

## 🤝 Contributing

We welcome contributions! Whether you're:
- Adding new industry examples
- Improving the UI/UX
- Enhancing documentation
- Fixing bugs or adding features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Databricks** for the incredible Agent Bricks platform
- **Streamlit** for the beautiful UI framework  
- **The Community** for inspiration and feedback
- **Cursor** for the seamless development experience

---

## 🚀 Ready to Transform Your Documents?

Whether you want the exact NFL & MLB rules assistant or need to create a knowledge base for your organization, this template gives you everything you need to go from documents to deployed AI assistant in minutes.

**Built with ❤️ using Databricks Agent Bricks and Streamlit**

*From sports rules to corporate policies - transform any document collection into an intelligent assistant!*
