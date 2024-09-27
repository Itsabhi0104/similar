import os
import lancedb
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import LanceDB

# Set OpenAI API Key
os.environ['OPENAI_API_KEY'] = "APIIIIII"

# Connect to LanceDB
conn = lancedb.connect("./company_data_db")

# Step 1: Search in the `company_embeddings` Table
table_embeddings = conn.open_table("company_embeddings")
if table_embeddings is None:
    raise ValueError("The table 'company_embeddings' could not be found.")

# Initialize OpenAI Embeddings
embedding_function = OpenAIEmbeddings()

# Example query
query = input("Ask me a question:")
query_embedding = embedding_function.embed_query(query)

# Perform similarity search on `company_embeddings` to find relevant companies
similar_companies_result = table_embeddings.search(query_embedding, vector_column_name="embedding").limit(2).to_pandas()

# Extract company symbols from the search results
similar_company_symbols = similar_companies_result['symbol'].tolist()

# Step 2: Fetch Company Details from the `company_profiles` Table using `symbol`
table_profiles = conn.open_table("company_profiles")
if table_profiles is None:
    raise ValueError("The table 'company_profiles' could not be found.")

company_details = []
for symbol in similar_company_symbols:
    # Filter the `company_profiles` table based on the symbol
    profile_result = table_profiles.to_pandas()
    company_profile = profile_result[profile_result['symbol'] == symbol]
    
    if not company_profile.empty:
        company_details.append(company_profile)

# Step 3: Display the company details
for company in company_details:
    print(company)
