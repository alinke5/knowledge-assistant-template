#!/usr/bin/env python3
"""
Simple script to test the Agent Bricks endpoint directly
This helps debug the exact input format expected by the endpoint
"""

import os
from mlflow.deployments import get_deploy_client
from openai import OpenAI

# Set your endpoint name
ENDPOINT_NAME = os.getenv('SERVING_ENDPOINT', 'YOUR_ENDPOINT_NAME')

def test_endpoint_formats():
    """Test various input formats to find the one that works"""
    test_question = "What is our company policy?"
    
    # Test OpenAI client format first (this should work based on playground example)
    print("\n🧪 Testing: OpenAI Client Format (Agent Bricks)")
    try:
        # Get Databricks token
        databricks_token = os.getenv('DATABRICKS_TOKEN')
        workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL', 'https://your-workspace.databricks.com')
        
        if not databricks_token:
            try:
                import dbutils
                databricks_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
            except:
                print("❌ Could not get Databricks token")
                databricks_token = "dummy_token"
        
        client = OpenAI(
            api_key=databricks_token,
            base_url=f"{workspace_url}/serving-endpoints"
        )
        
        response = client.responses.create(
            model=ENDPOINT_NAME,
            input=[
                {
                    "role": "user",
                    "content": test_question
                }
            ]
        )
        
        response_text = response.output[0].content[0].text
        print(f"✅ SUCCESS!")
        print(f"📥 Response: {response_text}")
        print(f"🎯 **OpenAI CLIENT FORMAT WORKS!**")
        return {"name": "OpenAI Client Format", "response": response_text}
        
    except Exception as e:
        print(f"❌ OpenAI Client Failed: {str(e)[:200]}...")
    
    # Fallback to MLflow testing
    print(f"\n🔄 Falling back to MLflow deployment client testing...")
    client = get_deploy_client('databricks')
    
    # Test formats based on CURL example - direct JSON payload
    formats_to_test = [
        # Format 1: Exact CURL format
        {
            "name": "CURL Format - Direct JSON",
            "inputs": {
                "input": [{"role": "user", "content": test_question}],
                "databricks_options": {
                    "return_trace": True
                }
            }
        },
        
        # Format 2: Minimal direct format
        {
            "name": "Minimal Direct Format",
            "inputs": {
                "input": [{"role": "user", "content": test_question}]
            }
        },
        
        # Format 3: Agent Bricks with instances wrapper
        {
            "name": "Agent Bricks - instances format",
            "inputs": {
                "instances": [
                    {
                        "input": [{"role": "user", "content": test_question}],
                        "max_output_tokens": 100
                    }
                ]
            }
        },
        
        # Format 4: Agent Bricks with additional fields
        {
            "name": "Agent Bricks - extended format",
            "inputs": {
                "inputs": {
                    "input": [{"role": "user", "content": test_question}],
                    "max_output_tokens": 100,
                    "temperature": 0.7,
                    "stream": False
                }
            }
        },
        
        # Format 5: dataframe_records with Agent schema
        {
            "name": "Agent Bricks - dataframe_records",
            "inputs": {
                "dataframe_records": [
                    {
                        "input": [{"role": "user", "content": test_question}],
                        "max_output_tokens": 100
                    }
                ]
            }
        },
        
        # Format 6: Minimal Agent Bricks
        {
            "name": "Agent Bricks - minimal",
            "inputs": {
                "inputs": {
                    "input": [{"role": "user", "content": test_question}]
                }
            }
        }
    ]
    
    for format_test in formats_to_test:
        print(f"\n🧪 Testing: {format_test['name']}")
        print(f"📤 Input: {format_test['inputs']}")
        
        try:
            response = client.predict(
                endpoint=ENDPOINT_NAME,
                inputs=format_test['inputs']
            )
            print(f"✅ SUCCESS!")
            print(f"📥 Response: {response}")
            print(f"🎯 **THIS FORMAT WORKS!**")
            return format_test
            
        except Exception as e:
            print(f"❌ Failed: {str(e)[:200]}...")
    
    print(f"\n❌ None of the formats worked. Check the endpoint documentation.")
    return None

if __name__ == "__main__":
    print("🔍 Testing Agent Bricks endpoint formats...")
    print(f"🎯 Endpoint: {ENDPOINT_NAME}")
    print(f"💡 Make sure to set SERVING_ENDPOINT environment variable!")
    
    working_format = test_endpoint_formats()
    
    if working_format:
        print(f"\n🎉 Found working format: {working_format['name']}")
        print(f"💡 Use this format in your app:")
        print(f"   inputs = {working_format['inputs']}")
    else:
        print(f"\n📞 Contact your Databricks admin for the exact endpoint schema")
        print(f"🔗 Endpoint: {ENDPOINT_NAME}")
        print(f"📋 Checklist:")
        print(f"   ✅ Set SERVING_ENDPOINT environment variable")
        print(f"   ✅ Verify endpoint name is correct")
        print(f"   ✅ Check endpoint permissions (CAN_QUERY)")
        print(f"   ✅ Ensure endpoint is in 'Ready' state")
