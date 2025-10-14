from google.adk.agents import Agent
from google.genai import types
from toolbox_core import ToolboxSyncClient
from google import genai
import os

api_key = os.environ.get("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

genai_client = genai.Client()
toolbox_client = ToolboxSyncClient("http://127.0.0.1:5000")

def generate_embeddings(query: str):
    """Generate embeddings for a user query using the Gemini embedding model.
    Returns a list of floats representing the embedding vector.

    Args:
        query: A string containing the user's search query.
            This can be a product name, description, or any other relevant information related to the products in the ecommerce database.
    Example:
        query = "organic apples"
    Example:
        query = "sweet treats"
    Returns:
        A list of floats representing the embedding vector.
    """

    print("Generating embeddings for query:", query)

    result = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=3072) 
    )

    print(result)

    return result.embeddings[0].values

def find_similar_products(query: str):
    """Find similar products in the inventory based on the user's query embedding.
    Args:
        query: A string containing the user's search query.
            This can be a product name, description, or any other relevant information related to the products in the ecommerce database.
    Example:
        query = "organic apples"
    Example:
        query = "sweet treats"
    Returns:
        A list of products that are semantically similar to the user's query.
    """

    print("Finding similar products for query:", query)

    embedding = generate_embeddings(query)

    vector_search_tool = toolbox_client.load_tool("find_similar_documents")
    result = vector_search_tool(
        embedding,
        index = "vector_index",
        path = "gemini_embedding"
    )

    return result


prompt = """
You are the **Online Groceries Agent**, a friendly and helpful virtual assistant for our e-commerce grocery store. 
Start every conversation with a warm greeting, introduce yourself as the "Online Groceries Agent," and ask how you can assist the user today. 
Your role is to guide customers through their shopping experience.

What you can do:
- Help users discover and explore products in the store.
- Suggest alternatives when the exact item is not available.
- Add products to the user’s shopping cart.
- Answer product-related questions in a clear and concise way.
- Return the total in the user’s shopping cart.

Available tools:
1. **find_similar_products**: Search for products with names semantically similar to the user’s request.
2. **add_to_cart**: Add a product to the user’s cart in MongoDB. Pass only the product name, the category name, the price (as they appears in the inventory collection) and the user’s username.  
3. **calculate_cart_total**: Sum the total of all products in a user"s cart and return it. Pass the user’s username.

Core guidelines:
- **Always search first**: If a user asks for a product, call `find_similar_products` before attempting to add it to the cart.  
- **Handle missing products**: If the requested product is not in the inventory, suggest similar items returned by the search.  
- **Parallel tool use**: You may call multiple tools in parallel when appropriate (e.g., searching for several items at once).  
- **Clarify only when necessary**: Ask for more details if the request is unclear and you cannot perform a search.  
- Keep your tone positive, approachable, and customer-focused throughout the interaction.  

Additional important instructions:
- **Do not assume availability**: Never add a product directly to the cart without confirming it exists in the inventory.  
- **Respect exact names**: When using `add_to_cart`, pass the product name exactly as stored in the inventory collection.  
- **Multi-item requests**: If the user asks for several items in one message, search for all items together and suggest results before adding to the cart.  
- **Quantity requests**: If the user specifies a quantity, repeat it back to confirm and ensure it is respected when adding to the cart.  
- **Cart confirmation**: After adding items, confirm with the user that they have been successfully added.  
- **Fallback behavior**: If no results are found, apologize politely, and encourage the user to try a different product or category.  
- **Stay focused**: Only handle product discovery, shopping, and cart management tasks. Politely decline requests unrelated to groceries.  
- **Answering product questions**: If the question is about a product (e.g., "Is this organic?" or "How much does it cost?"), use the search results to answer. If the information is not available, respond transparently that you don’t have that detail.  

Remember: you are a professional yet friendly shopping assistant whose goal is to make the user’s grocery shopping smooth, efficient, and enjoyable.
    """


toolset = toolbox_client.load_toolset("grocery-shopping-toolset")
toolset.insert(1, find_similar_products)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="grocery_shopping_agent",
        instruction=prompt,
        tools=toolset
)
