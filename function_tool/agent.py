from google.adk.agents import LlmAgent
from .salesforce_tool import salesforce_soql_tool

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.5-pro",
    tools=[salesforce_soql_tool],  # Pass the list of RestApiTool objects
    description="Salesforce query agent",
    instruction="""You are salesforce data explorer assistant managing query data from Salesforce.
    When query salesforce data, generate the SOQL query string based on the user request.
    Then, use the salesforce_soql_tool to query the data.
    Return the result to the user in a clear and informative manner.
    Caution: Only query built-in fields of Salesforce objects if user request is not specific.
    """,
)
