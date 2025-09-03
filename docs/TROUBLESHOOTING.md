# 🔧 Troubleshooting Guide

This guide helps you resolve common issues when setting up and running your Knowledge Assistant.

## 🚨 Common Issues

### 1. "Service Temporarily Unavailable" Error

#### Symptoms
- Red error message in the app
- "The endpoint is not compatible with this template"

#### Causes & Solutions

**Cause**: Agent Bricks not enabled
```bash
# Check if Agent Bricks is enabled in your workspace
# Contact your workspace admin to enable Agent Bricks (Beta)
```

**Cause**: Wrong endpoint name
```yaml
# In databricks.yml, verify your endpoint name
resources:
  serving-endpoints:
    serving-endpoint:
      name: "YOUR_ACTUAL_ENDPOINT_NAME"  # Check this matches exactly
```

**Cause**: Endpoint not ready
```bash
# Check endpoint status in Databricks UI
# Navigate to Serving > Endpoints > Your Endpoint
# Wait for status to be "Ready"
```

### 2. Authentication/Permission Errors

#### Symptoms
- "🔐 Authentication issue with the knowledge base"
- "CAN_QUERY permission required"

#### Solutions

**Grant Endpoint Permissions**
1. Go to Databricks workspace
2. Navigate to **Serving** > **Endpoints**
3. Click your endpoint name
4. Go to **Permissions** tab
5. Add user/group with **CAN_QUERY** permission

**Check Service Principal**
```yaml
# In databricks.yml, ensure correct principal
permissions:
  - level: CAN_QUERY
    principal: "{{workspace.current_user.userName}}"
```

**Verify Databricks CLI Auth**
```bash
databricks auth login
databricks workspace list  # Test connection
```

### 3. Sync/Deployment Issues

#### Symptoms
- "databricks sync" command fails
- Files not appearing in workspace

#### Solutions

**Check CLI Configuration**
```bash
databricks configure --list
databricks auth login --host https://your-workspace.databricks.com
```

**Verify Workspace Path**
```bash
# Make sure the path exists
databricks workspace ls /Workspace/Users/your.email@company.com/
```

**Permission Issues**
```bash
# Check you have workspace access
databricks workspace get-status /Workspace/Users/your.email@company.com/
```

### 4. Agent Creation Issues

#### Symptoms
- Agent creation fails or takes too long
- "Knowledge sources not syncing"

#### Solutions

**Check File Requirements**
- Files must be < 32MB
- Supported formats: txt, pdf, md, ppt/pptx, doc/docx
- Files must be in Unity Catalog volume

**Verify Unity Catalog Access**
```sql
-- Test access to your volume
SELECT * FROM information_schema.volumes 
WHERE volume_name = 'your_volume_name';
```

**Check Serverless Compute**
- Ensure serverless is enabled in workspace
- Check you have serverless budget allocation

### 5. App Runtime Errors

#### Symptoms
- App starts but crashes on questions
- "All approaches failed" error messages

#### Debug Steps

**Enable Debug Mode**
1. Temporarily change `app.yaml`:
   ```yaml
   command: ["streamlit", "run", "debug_app.py"]
   ```
2. Deploy and test each format
3. Switch back to main app

**Check Logs**
```bash
# In Databricks workspace, view app logs
# Click on your app > Logs tab
# Look for detailed error messages
```

**Test Endpoint Directly**
```python
# Use the test_endpoint.py script
python test_endpoint.py
```

### 6. Performance Issues

#### Symptoms
- Slow responses
- Timeouts
- High latency

#### Solutions

**Reduce Token Limit**
```python
# In app.py, reduce max_tokens
assistant_response = query_endpoint(
    endpoint_name=SERVING_ENDPOINT,
    messages=st.session_state.messages,
    max_tokens=128,  # Reduce for faster responses
)["content"]
```

**Check Endpoint Scaling**
- Verify endpoint has adequate compute resources
- Check for cold start delays

**Optimize Knowledge Base**
- Reduce document sizes
- Remove unnecessary files
- Optimize document structure

## 🔍 Debugging Techniques

### Enable Detailed Logging

```python
# Add to app.py for detailed debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
logger.debug(f"Querying endpoint: {SERVING_ENDPOINT}")
logger.debug(f"Message count: {len(st.session_state.messages)}")
```

### Test Endpoint Connectivity

```python
# Create a simple test script
from model_serving_utils import query_endpoint

try:
    response = query_endpoint(
        endpoint_name="your-endpoint-name",
        messages=[{"role": "user", "content": "test question"}],
        max_tokens=50
    )
    print("✅ Endpoint working:", response)
except Exception as e:
    print("❌ Endpoint failed:", str(e))
```

### Check Environment Variables

```python
# Add to your app for debugging
import os
st.sidebar.markdown("### 🐛 Debug Info")
st.sidebar.write(f"Endpoint: {os.getenv('SERVING_ENDPOINT')}")
st.sidebar.write(f"User: {get_user_info()}")
```

## 📋 Diagnostic Checklist

Before seeking help, verify:

### ✅ Prerequisites
- [ ] Agent Bricks enabled in workspace
- [ ] Unity Catalog enabled
- [ ] Serverless compute enabled
- [ ] Workspace in supported region (us-east-1, us-west-2)

### ✅ Agent Setup
- [ ] Knowledge Assistant created successfully
- [ ] Endpoint status is "Ready"
- [ ] Documents uploaded to Unity Catalog volume
- [ ] Agent has proper permissions

### ✅ App Configuration
- [ ] `databricks.yml` has correct endpoint name
- [ ] Databricks CLI configured and authenticated
- [ ] App files synced to workspace
- [ ] Dependencies installed correctly

### ✅ Permissions
- [ ] User has CAN_QUERY permission on endpoint
- [ ] User has workspace access
- [ ] Service principal configured correctly

## 🆘 Getting Help

### 1. Check Documentation
- [Agent Bricks Documentation](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/knowledge-assistant)
- [Databricks Apps Guide](https://docs.databricks.com/aws/en/dev-tools/databricks-apps)
- [Model Serving Troubleshooting](https://docs.databricks.com/aws/en/machine-learning/model-serving/troubleshooting)

### 2. Community Resources
- [Databricks Community Forums](https://community.databricks.com/)
- [GitHub Issues](https://github.com/your-repo/issues)
- Stack Overflow (tag: `databricks`)

### 3. Enterprise Support
- Open Databricks support ticket
- Contact your Customer Success Manager
- Reach out to your Databricks solutions architect

### 4. Collect Information for Support
When reporting issues, include:

```bash
# Workspace information
databricks --version
databricks configure --list

# Endpoint details
# Screenshot of endpoint status page
# Copy of error messages
# Relevant log excerpts
```

## 🐛 Known Issues & Workarounds

### Issue: Cold Start Delays
**Workaround**: Keep endpoint warm with periodic test calls

### Issue: Large Document Processing
**Workaround**: Split large documents into smaller chunks

### Issue: Special Characters in File Names
**Workaround**: Use simple ASCII file names

### Issue: VPN/Network Restrictions
**Workaround**: Check firewall rules for Databricks endpoints

## 🔄 Recovery Procedures

### Reset Your Agent
1. Delete current agent in Databricks UI
2. Wait 5 minutes
3. Recreate with same configuration
4. Update endpoint name in code

### Clean Workspace Sync
```bash
# Remove old files
databricks workspace delete /Workspace/Users/.../your-app/ --recursive

# Fresh sync
databricks sync . /Workspace/Users/.../your-app/
```

### Restart App
1. In Databricks workspace, go to your app
2. Click **Stop** if running
3. Wait 30 seconds
4. Click **Start**

Remember: Most issues are related to permissions or configuration. Double-check these first! 🔍
