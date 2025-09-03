#!/usr/bin/env python3
"""
Debug version of the app to test endpoint connectivity
"""

import os
import streamlit as st
from mlflow.deployments import get_deploy_client

st.title("🔍 Debug - Endpoint Connectivity Test")

SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT', 'YOUR_ENDPOINT_NAME')

st.write(f"**Testing endpoint:** `{SERVING_ENDPOINT}`")

if st.button("🧪 Test Endpoint Connection"):
    test_question = "What is our company policy on remote work?"
    
    st.write("**Testing different input formats...**")
    
    # Test 1: Direct JSON format (from curl example)
    try:
        st.write("**Test 1: Direct JSON Format (CURL format)**")
        client = get_deploy_client('databricks')
        
        # Direct format from curl example
        inputs = {
            "input": [{"role": "user", "content": test_question}],
            "databricks_options": {
                "return_trace": True
            }
        }
        
        st.code(f"Input format: {inputs}")
        
        response = client.predict(
            endpoint=SERVING_ENDPOINT,
            inputs=inputs
        )
        
        st.success("✅ Test 1 SUCCESS!")
        st.json(response)
        
    except Exception as e:
        st.error(f"❌ Test 1 Failed: {str(e)}")
    
    # Test 2: Minimal direct format
    try:
        st.write("**Test 2: Minimal Direct Format**")
        client = get_deploy_client('databricks')
        
        # Minimal direct format
        inputs = {
            "input": [{"role": "user", "content": test_question}]
        }
        
        st.code(f"Input format: {inputs}")
        
        response = client.predict(
            endpoint=SERVING_ENDPOINT,
            inputs=inputs
        )
        
        st.success("✅ Test 2 SUCCESS!")
        st.json(response)
        
    except Exception as e:
        st.error(f"❌ Test 2 Failed: {str(e)}")
    
    # Test 3: OpenAI Client approach (from playground)
    try:
        st.write("**Test 3: OpenAI Client (Playground Format)**")
        from openai import OpenAI
        
        # Try to get token
        databricks_token = os.getenv('DATABRICKS_TOKEN', 'dummy_token')
        workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL', 'https://your-workspace.databricks.com')
        
        client = OpenAI(
            api_key=databricks_token,
            base_url=f"{workspace_url}/serving-endpoints"
        )
        
        # Exact playground format
        input_data = [{"role": "user", "content": test_question}]
        
        st.code(f"OpenAI Client input: {input_data}")
        
        response = client.responses.create(
            model=SERVING_ENDPOINT,
            input=input_data
        )
        
        response_text = response.output[0].content[0].text
        
        st.success("✅ Test 3 SUCCESS!")
        st.write(f"**Response:** {response_text}")
        
    except Exception as e:
        st.error(f"❌ Test 3 Failed: {str(e)}")
    
    # Test 4: Check endpoint info
    try:
        st.write("**Test 4: Endpoint Information**")
        from databricks.sdk import WorkspaceClient
        w = WorkspaceClient()
        ep = w.serving_endpoints.get(SERVING_ENDPOINT)
        
        st.success("✅ Endpoint accessible!")
        st.write(f"**Task Type:** {ep.task}")
        st.write(f"**State:** {ep.state}")
        
    except Exception as e:
        st.error(f"❌ Endpoint info failed: {str(e)}")

st.markdown("---")
st.markdown("**Instructions:**")
st.markdown("1. Click the test button above")
st.markdown("2. Check which format works")
st.markdown("3. Use the working format in the main app")
st.markdown("4. Update your endpoint name in the environment variables")
