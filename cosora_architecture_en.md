## I. System Architecture

The system is structured into five main modules, clearly separating four fundamental responsibilities —knowledge preparation, information retrieval, flow orchestration, and response generation— supported by a cross-cutting shared tokenization module.

First, the **Ingestion and Indexing Module **is responsible for building the system’s knowledge base. To do so, it processes documents, splits them into chunks, tokenizes them using the shared **Tokenizer Module**, and generates their vector representations using an encoder-only language model (such as BERT). These embeddings are then stored in a vector database for use during the retrieval phase.

Second, the **Retrieval Module** is responsible for retrieving relevant context. This module receives queries (or sub-queries) already tokenized by the **Tokenizer Module**, generates their embeddings using the same encoder-only model, and performs similarity search over the vector database to identify the most relevant chunks, typically using efficient retrieval techniques such as Approximate Nearest Neighbor (ANN).

Third, the **Orchestration Module** acts as the central control layer of the system. This module receives the user query and dynamically determines the processing strategy. Optionally, it may activate a planning phase based on an LLM, which performs query decomposition to break the query into semantically independent sub-queries. The planning LLM is the same decoder-only model later used for response generation, operating in a differentiated planning mode through specific instructions. When this phase is not activated, the system operates directly on the original query.

Once the strategy is defined, the **Orchestrator** invokes the **Tokenizer Module**, which converts the query or sub-queries into token sequences. The tokenized sub-queries are then sent to the **Retrieval Module**, which generates their embeddings using the same encoder-only model and performs similarity search in the vector database to retrieve relevant chunks. Finally, the Orchestrator **aggregates** and consolidates the retrieved results to build the final prompt, which is passed to the **Generation Module** to produce the response.

Finally, the Tokenizer Module is a cross-cutting shared component, used by both the Ingestion and Indexing Module and the Orchestration Module. Its function is to ensure a consistent textual representation across all system phases, aligning the tokenization used for embedding generation and prompt construction.
Overall, the system is not limited to the interaction between two language models but is organized as a modular architecture in which two LLMs with differentiated roles operate in coordination —an encoder-only model for semantic representation through embeddings and a decoder-only model for response generation— together with specialized modules that manage indexing, retrieval, orchestration, and context preparation.

## II. Module Description

### 1. Ingestion and Indexing Module (offline)

#### Objective
To build the system’s indexed knowledge base.

#### Responsibilities

- Extracts content from documents and splits it into chunks.

- Tokenizes the chunks using the Tokenizer Module.

- Generates chunk embeddings using an encoder-only model (BERT).

- Stores embeddings in a vector database.

### 2. Retrieval Module (online)

##### Objective

To retrieve relevant context from the knowledge base.

##### Responsibilities

- Receives tokenized queries or sub-queries (from the Orchestration Module).

- Generates embeddings using an encoder-only model (BERT).

- Performs similarity search in the vector database (typically using Approximate Nearest Neighbor, ANN).

- Retrieves the top-k most relevant chunks.

- Reranking (optional).

### 3. Orchestration Module (online)

#### Objective

To coordinate system execution and define the retrieval and generation flow.

#### Responsibilities

- Receives the user query.

- Performs query decomposition using a planning LLM (optional).

- Invokes the Tokenizer Module to obtain the tokenized query (or tokenized sub-queries).

- Sends the tokenized query (or tokenized sub-queries) to the Retrieval Module.

- Receives retrieved chunks.

- Builds the final prompt (prompt assembly / prompt augmentation) by combining the query and retrieved context.

- Sends the final prompt to the Generation Module.

- Receives the response from the Generation Module.

- Returns the response to the user.

### 4. Generation Module (online)

#### Objective

To generate the final response conditioned on the retrieved context.

#### Responsibilities

- Receives the final prompt from the Orchestration Module.
- Generates the response (decoder-only LLM).
- Returns the response to the Orchestration Module.

### 5. Tokenizer Module (shared infrastructure)

#### Objective

To ensure consistency of textual representation across the entire system.

#### Responsibilities

- Tokenization of documents (Ingestion and Indexing Module).
- Tokenization of queries and sub-queries (Orchestration Module).

## III. LLMs

### 1. Encoder-only LLM for generating embeddings

[BSC-LT/MrBERT-es](https://huggingface.co/BSC-LT/MrBERT-es) is proposed as the encoder due to its Spanish specific optimization and its modern retrieval-oriented architecture, enabling the generation of semantically more accurate embeddings in Spanish-domain contexts compared to generic multilingual alternatives.

### 2. Decoder-only LLM decoder-only for generating responses

A GPT model pending to be specified

## IV. Base de datos vectorial

[ChromaDB](https://www.trychroma.com/products/chromadb) is proposed as the vector database due to its ease of integration, as it runs embedded in Python without requiring additional infrastructure, which facilitates rapid RAG prototyping. Furthermore, it enables efficient local persistence of embeddings and similarity queries, making it a lightweight and sufficient option for early-stage or experimental systems.