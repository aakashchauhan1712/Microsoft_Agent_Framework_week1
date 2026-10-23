# Microsoft Agent Framework — Week 1 AI Assistant

A conversational AI assistant built using **Microsoft Agent Framework (MAF)**, **Azure AI Foundry**, and **Streamlit**. This project demonstrates agent creation, tool calling, web search, and document-based question answering using Azure AI Foundry File Search.

## 🚀 Features

- **Conversational AI:** Answer general questions using a deployed GPT-4.1 mini model.
- **Mathematical Operations:** Perform addition and multiplication through agent tools.
- **Date and Time:** Retrieve the current local date and time.
- **Web Search:** Search the web using the Tavily API.
- **PDF Question Answering (RAG):** Upload a PDF, index it in Azure AI Foundry, and ask questions about its contents using File Search.
- **Interactive UI:** Chat with the agent through a Streamlit interface.
- **Tool Orchestration:** Use Microsoft Agent Framework to connect the model with callable Python tools.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Microsoft Agent Framework | Agent creation and tool orchestration |
| Azure AI Foundry | Model deployment and managed file search |
| GPT-4.1 mini | Conversational response generation |
| Streamlit | Interactive web interface |
| Azure Identity | Azure CLI authentication |
| Tavily | Web search |
| python-dotenv | Local environment configuration |

## 🏗️ Architecture

```text
                     User
                       |
                       v
                 Streamlit UI
                       |
                       v
            Microsoft Agent Framework
                       |
             Azure AI Foundry Client
                       |
          +------------+-------------+
          |            |             |
          v            v             v
      GPT-4.1 mini   Agent Tools   File Search
                     |             |
                +----+----+     Uploaded PDFs
                |    |    |
             Math  Date  Web Search
```

## 📂 Project Structure

```text
Week1_Streamlit/
├── app.py              # Streamlit application and chat interface
├── agent_logic.py      # Agent setup, tools, and PDF indexing logic
├── requirements.txt    # Python dependencies
├── .env                # Local configuration and secrets (not committed)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

## ⚙️ Prerequisites

Before running the application, ensure you have:

- Python 3.10 or a compatible version supported by your installed dependencies.
- An Azure account and an Azure AI Foundry project.
- A deployed GPT-4.1 mini model.
- Azure CLI installed and authenticated.
- A Tavily API key.
- Git and GitHub, if you want to clone or contribute to the repository.

## 🔧 Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/aakashchauhan1712/Microsoft_Agent_Framework_week1.git
cd Microsoft_Agent_Framework_week1
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=your_foundry_project_endpoint
FOUNDRY_MODEL=your_gpt_4_1_mini_deployment_name
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholders with your actual values. Use the **deployment name** for `FOUNDRY_MODEL` and the project endpoint from Azure AI Foundry.

Never commit your `.env` file, API keys, or access tokens to GitHub.

### 5. Authenticate with Azure

```powershell
az login
az account show
```

Confirm that the correct Azure subscription and account are selected and that you have the required permissions for your Foundry project.

### 6. Run the application

```powershell
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open that URL in your browser.

## 💬 Example Use Cases

### Mathematical calculations

**Prompt:**
> What is 125 multiplied by 48?

The agent can invoke the multiplication tool and return the result.

### Date and time

**Prompt:**
> What is the current date and time?

The agent can use the date/time tool rather than guessing.

### Web search

**Prompt:**
> Search the web for recent developments in agentic AI.

The agent can invoke the Tavily web-search tool.

### PDF question answering

1. Upload a PDF using the sidebar.
2. Select **Process PDF**.
3. Wait for the indexing-success message.
4. Ask a question about the document.

The agent can use Foundry File Search to retrieve relevant document content and formulate an answer.

## 🧠 Key Concepts Learned

- Creating AI agents using Microsoft Agent Framework.
- Connecting agents to Azure AI Foundry.
- Defining Python functions as callable agent tools.
- Understanding tool calling and agent orchestration.
- Maintaining conversation state in Streamlit.
- Using asynchronous Python operations in an interactive application.
- Uploading and indexing PDF documents.
- Implementing document-based question answering using managed file search.
- Managing configuration and credentials securely.

## 🔐 Security Notes

- Keep `.env` out of version control.
- Do not hardcode API keys or credentials.
- Use Azure CLI authentication for local development.
- Review uploaded documents before processing them.
- Apply appropriate access controls and data-retention policies before deploying the application for wider use.

## 🚧 Future Improvements

- Display document citations and page references in answers.
- Support multiple PDFs and persistent knowledge bases.
- Add automated tests for tools and document retrieval.
- Improve error handling and logging.
- Add conversation export and document-management controls.
- Deploy the application to a suitable hosting environment.
- Evaluate answer quality, retrieval relevance, and tool-call accuracy.

## 👨‍💻 Author

**Akash Chauhan**

GitHub: [@aakashchauhan1712](https://github.com/aakashchauhan1712)

---

*Built as part of a hands-on learning journey with Microsoft Agent Framework and Azure AI Foundry.*
