from mlflow.deployments import get_deploy_client
from databricks.sdk import WorkspaceClient
from openai import OpenAI
import os

def _get_endpoint_task_type(endpoint_name: str) -> str:
    """Get the task type of a serving endpoint."""
    w = WorkspaceClient()
    ep = w.serving_endpoints.get(endpoint_name)
    return ep.task

def is_endpoint_supported(endpoint_name: str) -> bool:
    """Check if the endpoint has a supported task type."""
    try:
        task_type = _get_endpoint_task_type(endpoint_name)
        # Support various agent and chat endpoint types
        supported_task_types = [
            "agent/v1/chat", 
            "agent/v2/chat", 
            "llm/v1/chat",
            "AGENT_TASK",  # Agent Bricks endpoints
            "agent",       # Generic agent endpoints
            "chat"         # Generic chat endpoints
        ]
        
        # Check if task_type contains agent or chat (case insensitive)
        task_lower = task_type.lower() if task_type else ""
        direct_match = task_type in supported_task_types
        contains_agent = "agent" in task_lower
        contains_chat = "chat" in task_lower
        
        return direct_match or contains_agent or contains_chat
    except Exception as e:
        # If we can't determine the task type, assume it's supported and let the query fail gracefully
        print(f"Warning: Could not determine endpoint task type: {e}")
        return True

def _validate_endpoint_task_type(endpoint_name: str) -> None:
    """Validate that the endpoint has a supported task type."""
    if not is_endpoint_supported(endpoint_name):
        raise Exception(
            f"Detected unsupported endpoint type for this chatbot template. "
            f"This chatbot template only supports chat completions-compatible endpoints. "
            f"For a richer chatbot template with support for all conversational endpoints on Databricks, "
            f"see https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app"
        )

def _query_endpoint(endpoint_name: str, messages: list[dict[str, str]], max_tokens) -> list[dict[str, str]]:
    """Calls an Agent Bricks endpoint using direct JSON format."""
    _validate_endpoint_task_type(endpoint_name)
    
    # Agent Bricks expects DIRECT JSON payload (not wrapped in dataframe_records/instances)
    try:
        # Format messages for Agent Bricks
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Direct JSON payload format (from curl example)
        payload = {
            "input": formatted_messages,
            "databricks_options": {
                "return_trace": True
            }
        }
        
        res = get_deploy_client('databricks').predict(
            endpoint=endpoint_name,
            inputs=payload,  # Direct payload, not wrapped
        )
        
        # Handle Agent Bricks direct response format
        if "output" in res:
            # Direct Agent Bricks response
            output = res["output"]
            if isinstance(output, list) and len(output) > 0:
                first_output = output[0]
                if isinstance(first_output, dict) and "content" in first_output:
                    content_list = first_output["content"]
                    if isinstance(content_list, list) and len(content_list) > 0:
                        # Extract text from content
                        content_item = content_list[0]
                        if isinstance(content_item, dict) and "text" in content_item:
                            return [{"role": "assistant", "content": content_item["text"]}]
                        return [{"role": "assistant", "content": str(content_item)}]
                return [{"role": "assistant", "content": str(first_output)}]
            return [{"role": "assistant", "content": str(output)}]
        elif "predictions" in res and len(res["predictions"]) > 0:
            # Fallback to predictions format
            prediction = res["predictions"][0]
            if isinstance(prediction, str):
                return [{"role": "assistant", "content": prediction}]
            elif isinstance(prediction, dict) and "content" in prediction:
                return [{"role": "assistant", "content": prediction["content"]}]
        
        return [{"role": "assistant", "content": str(res)}]
        
    except Exception as e:
        # Try alternative direct format (without databricks_options)
        try:
            # Simplified direct format
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Minimal direct payload
            payload = {
                "input": formatted_messages
            }
            
            res = get_deploy_client('databricks').predict(
                endpoint=endpoint_name,
                inputs=payload,
            )
            
            # Handle response same as above
            if "output" in res:
                output = res["output"]
                if isinstance(output, list) and len(output) > 0:
                    first_output = output[0]
                    if isinstance(first_output, dict) and "content" in first_output:
                        content_list = first_output["content"]
                        if isinstance(content_list, list) and len(content_list) > 0:
                            content_item = content_list[0]
                            if isinstance(content_item, dict) and "text" in content_item:
                                return [{"role": "assistant", "content": content_item["text"]}]
                            return [{"role": "assistant", "content": str(content_item)}]
                    return [{"role": "assistant", "content": str(first_output)}]
                return [{"role": "assistant", "content": str(output)}]
            return [{"role": "assistant", "content": str(res)}]
            
        except Exception as e2:
            # Final attempt with OpenAI client (if token available)
            try:
                # Get Databricks token
                databricks_token = os.getenv('DATABRICKS_TOKEN')
                if not databricks_token:
                    # In Databricks Apps, token might be available through service principal
                    try:
                        from databricks.sdk import WorkspaceClient
                        w = WorkspaceClient()
                        databricks_token = w.config.token
                    except:
                        raise Exception("No authentication token available")
                
                # Get workspace URL from environment or workspace client
                workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')
                if not workspace_url:
                    try:
                        from databricks.sdk import WorkspaceClient
                        w = WorkspaceClient()
                        workspace_url = w.config.host
                    except:
                        raise Exception("No workspace URL available")
                
                # Initialize OpenAI client with Databricks endpoint
                client = OpenAI(
                    api_key=databricks_token,
                    base_url=f"{workspace_url}/serving-endpoints"
                )
                
                # Call the Agent Bricks endpoint using OpenAI format (exact playground format)
                response = client.responses.create(
                    model=endpoint_name,
                    input=messages  # Pass messages in exact playground format
                )
                
                # Extract the response text from Agent Bricks format
                response_text = response.output[0].content[0].text
                return [{"role": "assistant", "content": response_text}]
                
            except Exception as e3:
                raise Exception(f"All approaches failed. MLflow1: {e}, MLflow2: {e2}, OpenAI: {e3}")


def query_endpoint(endpoint_name, messages, max_tokens):
    """
    Query a chat-completions or agent serving endpoint
    If querying an agent serving endpoint that returns multiple messages, this method
    returns the last message
    ."""
    return _query_endpoint(endpoint_name, messages, max_tokens)[-1]
