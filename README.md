# Google Cloud MCP Toolbox Demo

This repository contains a small demo agent that uses Google Gemini embeddings and an [MCP Toolbox](https://github.com/googleapis/genai-toolbox) MongoDB toolset to implement an "Online Groceries Agent". The agent demonstrates how to search for products in an inventory using vector search, add products to a cart (MongoDB collection) and get the cart total (aggregating the cart collection). 

- `mongodb-groceries-agent/`: Contains the demo agent implementation (`agent.py`) and package init.
- `tools.yaml`: Toolbox toolset definition for the MongoDB tools.

## Prerequisites

Before running the demo, ensure you have the following installed and available on your machine:

- Python 3.10+ (3.11 recommended)
- pip (or an equivalent Python package manager)
- MCP Toolbox Server (follow the [instructions](https://googleapis.github.io/genai-toolbox/getting-started/introduction/#installing-the-server))
- A Google API key with access to the GenAI services (set as `GOOGLE_API_KEY` environment variable)
- A MongoDB deployment (Atlas free M0 cluster is supported — instructions below)

## Setting up a free MongoDB Atlas M0 cluster

You can create a free (M0) MongoDB Atlas cluster. Follow these steps:

1. Open the Atlas [registration page in your browser](https://www.mongodb.com/try?utm_campaign=devrel&utm_source=youtube&utm_medium=cta&utm_content=mcp.toolbox&utm_term=stanimira.vlaeva).
2. Sign up for a free MongoDB account or sign in if you already have one.
3. Click "Create a Cluster" and choose the free tier (M0 / Shared).
4. Choose a cloud provider and region (defaults are fine for the demo).
5. Create a database user: go to "Database Access" and add a user with a password. Save this username/password — you'll need it for connection strings.
6. Allow your IP address: go to "Network Access" and add your current IP or 0.0.0.0/0 for testing (not recommended for production).
7. Click "Connect", choose "Connect your application", and copy the provided connection string.

    Use the connection string in `tools.yaml` as the `uri` or preferrably, set it through an environment variables. An example connection string looks like:

    ```
    mongodb+srv://<username>:<password>@<your-cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
    ```

    Note: Replace `<username>`, `<password>`, `<your-cluster>` and `<dbname>` with values from Atlas. For local testing you can also use a local MongoDB server.

8. Import the sample grocery products data into a collection named `products` in a database named `groceries`. You can use the provided `sample_data/groceries.json` file and the MongoDB Atlas UI or `mongosh` to import it.

```
mongoimport --uri="<your-connection-string>" --db="grocery_store" --collection="inventory" --file="grocery_store.inventory.json" --jsonArray

```
## Configuration

Set the following environment variables before running the agent:

- `GOOGLE_API_KEY` — your Google GenAI API key

Example (macOS / zsh):

```bash
export GOOGLE_API_KEY="your-google-api-key"
```

## Running the demo agent

1. Install dependencies (adjust if this repo is part of a larger project). From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if a requirements file exists; otherwise install needed packages manually
```

2. Start the toolbox server:

```bash
./toolbox --tools-file "tools.yaml"
```

3. Ensure the Toolbox server is running and accessible at `http://127.0.0.1:5000`.

3. Run the agent code (this demo file is intended to be imported by an orchestration script that starts the agent). To quickly try a simple run or import the module:

```python
adk web
```

Adjust calls as needed to integrate the agent into a runtime environment that manages the Agent lifecycle.

## What `agent.py` does

- Reads `GOOGLE_API_KEY` from the environment and sets it on `os.environ` for the Google GenAI client.
- Creates a `genai.Client()` and a Toolbox client targeting `http://127.0.0.1:5000`.
- Provides `generate_embeddings(query)` to produce embedding vectors using `gemini-embedding-001`.
- Provides `find_similar_products(query)` which runs a vector search via the toolbox tool `find_similar_documents` against an index named `vector_index` and the field `gemini_embedding`.
- Builds an `Agent` configured to use those tools and a `grocery-shopping-toolset` loaded from the toolbox.

## Troubleshooting

- If you get authentication errors from GenAI, confirm `GOOGLE_API_KEY` is set and valid.
- If the Toolbox client cannot connect, confirm the ToolboxSync server is running and reachable at the configured address.
- If MongoDB connection issues appear, verify your Atlas IP allowlist and database user credentials.

## Contributors ✨

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center">
        <a href="https://www.linkedin.com/in/sis0k0/">
            <img src="https://avatars.githubusercontent.com/u/7893485?v=4" width="100px;" alt=""/><br />
            <sub><b>Stanimira Vlaeva</b></sub>
        </a><br />
    </td>
  </tr>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

## Disclaimer

Use at your own risk; not a supported MongoDB product
