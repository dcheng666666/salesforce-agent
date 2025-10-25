import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

salesforce_mcp_tool = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@tsmztech/mcp-server-salesforce",
            ],
            env={
                "SALESFORCE_CONNECTION_TYPE": os.getenv("SALESFORCE_CONNECTION_TYPE", "OAuth_2.0_Client_Credentials"),
                "SALESFORCE_CLIENT_ID": os.getenv("SALESFORCE_CLIENT_ID"),
                "SALESFORCE_CLIENT_SECRET": os.getenv("SALESFORCE_CLIENT_SECRET"),
                "SALESFORCE_INSTANCE_URL": os.getenv("SALESFORCE_MY_DOMAIN_URL"),
            },
        )
    )
)

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.5-pro",
    tools=[salesforce_mcp_tool],  # Pass the list of RestApiTool objects
    description="Salesforce query agent",
    instruction="""You are salesforce data explorer assistant managing query data from Salesforce.
    When query salesforce data, generate the SOQL query string based on the user request.
    Then, use the salesforce_mcp_tool to query the data.
    Return the result to the user in a clear and informative manner.
    Caution: Only query built-in fields of Salesforce objects if user request is not specific.
    """,
)
