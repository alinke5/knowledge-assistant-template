# 🚀 Complete Setup Guide

This guide will walk you through setting up your own Knowledge Assistant using Databricks Agent Bricks.

## Prerequisites

### Databricks Workspace Requirements
- **Agent Bricks enabled** (Beta feature)
- **Unity Catalog enabled**
- **Serverless compute enabled**
- **Model Serving access**
- **Workspace in supported regions**: `us-east-1` or `us-west-2`

### Local Environment
- **Databricks CLI** installed and configured
- **Python 3.8+**
- **Git** for version control

## Step 1: Prepare Your Documents

### Supported File Types
- `.txt` - Plain text files
- `.pdf` - PDF documents (recommended < 32MB)
- `.md` - Markdown files
- `.ppt/.pptx` - PowerPoint presentations
- `.doc/.docx` - Word documents

### Upload to Unity Catalog
1. **Create a Volume**
   ```sql
   CREATE VOLUME IF NOT EXISTS main.default.knowledge_docs;
   ```

2. **Upload Your Files**
   - Use Databricks UI to upload files to the volume
   - Or use CLI: `databricks fs cp your-files/ /Volumes/main/default/knowledge_docs/`

## Step 2: Create Agent Bricks Knowledge Assistant

### Through Databricks UI
1. **Navigate to Agents**
   - Go to your Databricks workspace
   - Click **Agents** in the left navigation
   - Click **Knowledge Assistant**

2. **Configure Your Agent**
   - **Name**: Choose a descriptive name (e.g., "Company-Policy-Assistant")
   - **Description**: Describe what your agent can help with
   - **Knowledge Source**: Select your Unity Catalog volume
   - **Instructions**: Add any specific guidelines for responses

3. **Deploy**
   - Click **Create Agent**
   - Wait for processing (can take up to a few hours)
   - Note your endpoint name for later use

### Example Configuration
```yaml
Name: HR Policy Assistant
Description: AI assistant for company HR policies and procedures
Knowledge Source: /Volumes/main/default/hr_policies/
Instructions: |
  Please provide helpful, accurate information about company policies.
  Always cite the source document when possible.
  If you're unsure about something, direct users to HR for clarification.
```

## Step 3: Test Your Agent

### In AI Playground
1. **Open Playground**
   - Click **Try in Playground** from your agent dashboard
   - Test with sample questions
   - Verify citations are working

### Example Test Questions
- "What is the remote work policy?"
- "How do I request vacation time?"
- "What are the benefits enrollment deadlines?"

## Step 4: Clone and Configure This App

### Clone Repository
```bash
git clone https://github.com/your-username/knowledge-assistant-template
cd knowledge-assistant-template
```

### Update Configuration Files

#### 1. databricks.yml
```yaml
resources:
  serving-endpoints:
    serving-endpoint:
      name: "YOUR_AGENT_ENDPOINT_NAME"  # Replace with your endpoint name
      permissions:
        - level: CAN_QUERY
          principal: "{{workspace.current_user.userName}}"
```

#### 2. Customize app.py
Update the header and branding:
```python
# Change the title and subtitle
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏢 Your Company Knowledge Assistant 📚</h1>
    <p class="main-subtitle">Your AI-powered expert for company policies</p>
</div>
""", unsafe_allow_html=True)
```

Update example questions:
```python
example_questions = [
    "What is our remote work policy?",
    "How do I request time off?",
    "What are the company benefits?",
    "Where can I find the employee handbook?"
]
```

## Step 5: Deploy to Databricks

### Sync Your Code
```bash
# Replace with your workspace path
databricks sync . /Workspace/Users/your.email@company.com/knowledge-assistant-app
```

### Deploy Through Databricks Apps
1. **Navigate to your workspace**
2. **Go to your synced folder**
3. **Deploy using Databricks Apps**
   - Right-click on the folder
   - Select **Deploy as App**
   - Follow the deployment wizard

## Step 6: Access Your App

### Get Your App URL
- After deployment, Databricks will provide a URL
- Share this URL with your users
- Access is controlled by Databricks workspace permissions

### Example URL Format
```
https://your-workspace.databricks.com/apps/your-app-name
```

## Troubleshooting

### Common Issues

#### "Endpoint not found"
- Verify your endpoint name in `databricks.yml`
- Check that the endpoint is deployed and ready
- Ensure you have CAN_QUERY permissions

#### "Service Temporarily Unavailable"
- Check if Agent Bricks is enabled in your workspace
- Verify your workspace is in a supported region
- Check serverless compute is enabled

#### "Authentication errors"
- Verify Databricks CLI is configured: `databricks auth login`
- Check workspace permissions
- Ensure service principal has correct access

#### "Sync fails"
- Check your Databricks CLI configuration
- Verify workspace path exists
- Check file permissions

### Getting Help

1. **Check Databricks Documentation**
   - [Agent Bricks Guide](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/knowledge-assistant)
   - [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps)

2. **Community Support**
   - Databricks Community Forums
   - GitHub Issues in this repository

3. **Enterprise Support**
   - Contact your Databricks customer success team
   - Open a support ticket through Databricks portal

## Next Steps

- **Customize the UI** further (see [CUSTOMIZATION.md](CUSTOMIZATION.md))
- **Add more knowledge sources** to your Agent Bricks
- **Set up monitoring** and feedback collection
- **Train your team** on using the assistant

Congratulations! You now have a fully functional knowledge assistant! 🎉
