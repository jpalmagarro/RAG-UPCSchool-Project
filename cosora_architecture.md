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