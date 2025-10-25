# Salesforce Agent

An intelligent Salesforce data query agent built with Google ADK and Gemini LLM model for querying Salesforce data via SOQL.

## 🎯 Codebase Purpose

This codebase demonstrates **two different approaches** for integrating Salesforce with AI agents:

1. **Function Tool Approach** (`function_tool/`): Wraps Salesforce API calls as custom function tools that the agent can directly invoke
2. **MCP (Model Context Protocol) Approach** (`salesforce_mcp/`): Uses the Salesforce MCP server to provide standardized tool interfaces for agent interaction

Both approaches showcase how to encapsulate Salesforce connectivity and operations into reusable tools that AI agents can leverage for data querying and manipulation.

## 🛠 Tech Stack

- **AI Framework**: [Google ADK](https://github.com/google/adk) (v1.17.0+)
- **LLM Model**: Gemini
- **Language**: Python 3.12+
- **Package Manager**: uv
- **API Integration**: Salesforce REST API (OAuth 2.0)

## 📋 Prerequisites

1. **Python 3.12 or higher**
2. **Google Cloud Account** (for accessing Gemini API)
3. **Salesforce Account** with configured External Client App
4. **uv** package manager

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd salesforce-agent
```

### 2. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

## ⚙️ Configuration

### 1. Create Environment Variables File

Copy `env.example` to `.env`:
```bash
cp env.example .env
```

### 2. Configure Google Cloud

Set the following variables in your `.env` file:

```bash
# Google Cloud Configuration
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id_here
GOOGLE_CLOUD_LOCATION=your_google_cloud_region_here
```

### 3. Configure Salesforce External Client App

#### Create a Salesforce External Client App:

1. **Log in to Salesforce** and navigate to "Setup"

2. **Create a new External Client App**:
   - Search for and navigate to "External Client App Manager"
   - Click "New External Client App"

3. **Fill in Basic Information**:
   - App Name: Custom application name
   - API Name: Auto-generated
   - Description: Application description (optional)
   - Contact Email: Your email address

4. **Configure API Settings** (API - Enable OAuth Settings):
   - Callback URL: `https://localhost:8080/callback` (or your callback URL)
   - Selected OAuth Scopes: Choose based on requirements, at minimum include:
     - "Manage user data via APIs (api)"
     - "Perform requests at any time (refresh_token, offline_access)"

5. **Enable OAuth Flow** (Flow Enablement):
   - Check "Enable Client Credentials Flow" (for server-to-server authentication)
   - Optionally enable other flows as needed (e.g., Authorization Code Flow)

6. **Configure Run As User**:
   - In the Policies tab, enable client credentials flow and configure "Run As User" section
   - The permissions of this user determine what data and functionality the API calls can access


7. **Save and Activate**:
   - Click "Save" to save the configuration
   - Ensure the application status is "Active"
   - Record the Consumer Key and Consumer Secret

#### Configure in `.env`:

```bash
# Salesforce Authentication Configuration
SALESFORCE_CLIENT_ID=your_consumer_key_here
SALESFORCE_CLIENT_SECRET=your_consumer_secret_here
SALESFORCE_MY_DOMAIN_URL=https://yourcompany.my.salesforce.com
SALESFORCE_API_VERSION=v64.0
```

### 4. Start ADK Web Application

#### Activate Python Virtual Environment

```bash
# If using a virtual environment created by uv
source .venv/bin/activate
```

#### Start the Application

```bash
adk web
```

After the application starts, the access address will be displayed in the terminal (usually `http://localhost:8000`). Open this address in your browser to use the Salesforce Agent.


## 💡 Usage Examples

### Example 1: Query Specific Company Account

**User Input:**
```
I want to know Huawei Account in My CRM
```

## 📝 Important Notes

1. **Security**:
   - Never commit the `.env` file to version control
   - Regularly rotate Salesforce Client Secret


## 🔗 Related Links

- [Google ADK Documentation](https://github.com/google/adk)
- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [SOQL Query Language Guide](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/)
