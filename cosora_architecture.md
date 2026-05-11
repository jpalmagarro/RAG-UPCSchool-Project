## I. Arquitectura del sistema

El sistema se estructura en cinco módulos principales, que separan de forma clara cuatro responsabilidades fundamentales —preparación del conocimiento, recuperación de información, orquestación del flujo y generación de respuestas— apoyadas por un módulo transversal de tokenización compartida. 

En primer lugar, el **Ingestion and Indexing Module** se encarga de construir la base de conocimiento del sistema. Para ello, procesa los documentos, los divide en chunks, los tokeniza mediante el **Tokenizer Module** compartido y genera sus representaciones vectoriales utilizando un modelo de lenguaje de tipo encoder-only (como BERT). Estos embeddings se almacenan posteriormente en una base de datos vectorial para su uso en fase de recuperación.

En segundo lugar, el **Retrieval Module** es responsable de recuperar el contexto relevante. Este módulo recibe las queries (o sub-queries) ya tokenizadas por el **Tokenizer Module**, genera sus embeddings mediante el mismo modelo encoder-only y realiza la búsqueda por similitud sobre la base de datos vectorial para identificar los chunks más relevantes, típicamente mediante técnicas eficientes de recuperación como _Approximate Nearest Neighbor_ (ANN).

En tercer lugar, el **Orchestration Module** actúa como la capa central de control del sistema. Este módulo recibe la query del usuario y determina dinámicamente la estrategia de procesamiento. De forma opcional, puede activar una fase de planificación basada en un LLM, que realiza query decomposition para descomponer la consulta en sub-queries semánticamente independientes. El LLM de planificación es el mismo modelo decoder-only utilizado posteriormente en la generación de respuestas, operando en un modo de planificación diferenciado mediante instrucciones específicas. Cuando esta fase no se activa, el sistema opera directamente sobre la query original.

Una vez definida la estrategia, el **Orchestrator** invoca el **Tokenizer Module**, que convierte la query o las sub-queries en secuencias de tokens. A continuación, las sub-queries tokenizadas se envían al **Retrieval Module**, que genera sus embeddings mediante el mismo modelo encoder-only y realiza la búsqueda por similitud en la base de datos vectorial para recuperar los chunks relevantes. Finalmente, el **Orchestrator** agrega y consolida los resultados obtenidos para construir el prompt final, que es utilizado por el **Generation Module** para producir la respuesta.

Finalmente, el **Tokenizer Module** constituye un componente transversal compartido, utilizado tanto por el Ingestion and Indexing Module como por el Orchestration Module. Su función es garantizar una representación textual consistente en todas las fases del sistema, alineando la tokenización empleada en la generación de embeddings y en la construcción de prompts.

En conjunto, el sistema no se limita a la interacción entre dos modelos de lenguaje, sino que se organiza como una arquitectura modular en la que intervienen de forma coordinada dos LLMs con roles diferenciados —un modelo encoder-only para la representación semántica mediante embeddings y un modelo decoder-only para la generación de respuestas— junto con módulos especializados que gestionan la indexación, la recuperación, la orquestación y la preparación del contexto.

## II. Descripción de módulos

### 1. Ingestion and Indexing Module (offline)

#### Objetivo
Construir la base de conocimiento indexada del sistema.

#### Responsabilidades
   
- Extrae el contenido de los documentos y lo divide en chunks.
    
- Tokeniza los chunks mediante el Tokenizer Module.

- Genera embeddings de los chunks mediante modelo encoder-only (BERT).

- Almacena los embeddings en una base de datos vectorial.
      

### 2. Retrieval Module (online)

##### Objetivo

Recuperar contexto relevante de la base de conocimiento.

##### Responsabilidades

- Recibe query o sub-queries ya tokenizadas (provenientes del Orchestration Module).

- Genera embeddings mediante modelo encoder-only (BERT).

- Realiza búsqueda por similitud en base de datos vectorial (típicamente con _Approximate Nearest Neighbor_, ANN).

- Obtiene los top-k chunks más relevantes.

- Reranking (opcional).

### 3. Orchestration Module (online)

##### Objetivo

Coordinar la ejecución del sistema y definir el flujo de recuperación y generación.

##### Responsabilidades

- Recibe query del usuario.
    
- Query decomposition mediante LLM de planificación (opcional).

- Invoca al Tokenizer Module para obtener la query tokenizada (o las sub-queries tokenizadas).

- Envía la query tokenizada (o las sub-queries tokenizadas) al Retrieval Module.

- Recibe chunks recuperados.

- Construye el prompt final (prompt assembly / prompt augmentation) combinando la query y el contexto recuperado.

- Envía el prompt final al Generation Module.

- Recibe la respuesta del Generation Module.

- Envía la respuesta al usuario.
   
### 4. Generation Module (online)

##### Objetivo

Generar la respuesta final condicionada al contexto recuperado.

##### Responsabilidades

- Recibe el prompt final del Orchestration Module.
- Genera la respuesta (LLM decoder-only).
- Devuelve la respuesta al Orchestration Module.
 

### 5. Tokenizer Module (shared infrastructure)

##### Objetivo

Garantizar consistencia de la representación textual en todo el sistema.

##### Responsabilidades

- Tokenización de documentos (Ingestion and Indexing Module).
- Tokenización de queries y sub-queries (Orchestration Module)

English Translation 
I. System Architecture


The system is structured into five main modules, clearly separating four fundamental responsibilities —knowledge preparation, information retrieval, flow orchestration, and response generation— supported by a cross-cutting shared tokenization module.

First, the Ingestion and Indexing Module is responsible for building the system’s knowledge base. To do so, it processes documents, splits them into chunks, tokenizes them using the shared Tokenizer Module, and generates their vector representations using an encoder-only language model (such as BERT). These embeddings are then stored in a vector database for use during the retrieval phase.

Second, the Retrieval Module is responsible for retrieving relevant context. This module receives queries (or sub-queries) already tokenized by the Tokenizer Module, generates their embeddings using the same encoder-only model, and performs similarity search over the vector database to identify the most relevant chunks, typically using efficient retrieval techniques such as Approximate Nearest Neighbor (ANN).

Third, the Orchestration Module acts as the central control layer of the system. This module receives the user query and dynamically determines the processing strategy. Optionally, it may activate a planning phase based on an LLM, which performs query decomposition to break the query into semantically independent sub-queries. The planning LLM is the same decoder-only model later used for response generation, operating in a differentiated planning mode through specific instructions. When this phase is not activated, the system operates directly on the original query.
Once the strategy is defined, the Orchestrator invokes the Tokenizer Module, which converts the query or sub-queries into token sequences. The tokenized sub-queries are then sent to the Retrieval Module, which generates their embeddings using the same encoder-only model and performs similarity search in the vector database to retrieve relevant chunks. Finally, the Orchestrator aggregates and consolidates the retrieved results to build the final prompt, which is passed to the Generation Module to produce the response.

Finally, the Tokenizer Module is a cross-cutting shared component, used by both the Ingestion and Indexing Module and the Orchestration Module. Its function is to ensure a consistent textual representation across all system phases, aligning the tokenization used for embedding generation and prompt construction.
Overall, the system is not limited to the interaction between two language models but is organized as a modular architecture in which two LLMs with differentiated roles operate in coordination —an encoder-only model for semantic representation through embeddings and a decoder-only model for response generation— together with specialized modules that manage indexing, retrieval, orchestration, and context preparation.

II. Module Description
1. Ingestion and Indexing Module (offline)
Objective
To build the system’s indexed knowledge base.
Responsibilities
Extracts content from documents and splits it into chunks.
Tokenizes the chunks using the Tokenizer Module.
Generates chunk embeddings using an encoder-only model (BERT).
Stores embeddings in a vector database.

2. Retrieval Module (online)
Objective
To retrieve relevant context from the knowledge base.
Responsibilities
Receives tokenized queries or sub-queries (from the Orchestration Module).
Generates embeddings using an encoder-only model (BERT).
Performs similarity search in the vector database (typically using Approximate Nearest Neighbor, ANN).
Retrieves the top-k most relevant chunks.
Optional reranking.

3. Orchestration Module (online)
Objective
To coordinate system execution and define the retrieval and generation flow.
Responsibilities
Receives the user query.
Performs query decomposition using a planning LLM (optional).
Invokes the Tokenizer Module to obtain the tokenized query (or tokenized sub-queries).
Sends the tokenized query (or tokenized sub-queries) to the Retrieval Module.
Receives retrieved chunks.
Builds the final prompt (prompt assembly / prompt augmentation) by combining the query and retrieved context.
Sends the final prompt to the Generation Module.
Receives the response from the Generation Module.
Returns the response to the user.

4. Generation Module (online)
Objective
To generate the final response conditioned on the retrieved context.
Responsibilities
Receives the final prompt from the Orchestration Module.
Generates the response (decoder-only LLM).
Returns the response to the Orchestration Module.

5. Tokenizer Module (shared infrastructure)
Objective
To ensure consistency of textual representation across the entire system.
Responsibilities
Tokenization of documents (Ingestion and Indexing Module).
Tokenization of queries and sub-queries (Orchestration Module).
