# Infinite Agent

Proposed architecture for a general-purpose agent with function calling and relational database retrieval.

```mermaid
flowchart TD
    U[User message] --> S[Accumulate requests and prior results]
    S --> A[Immediate receipt acknowledgement<br/>once per received message]
    A --> D[Select all required functions<br/>no fixed count limit]
    FR[Function descriptions] -.-> D
    D --> P[Prepare function inputs]
    P -->|Database lookup| T[Select schema or registered SQL]
    DB[Schema descriptions<br/>relation links and registered SQL] -.-> T
    P -->|Other function| K[Reuse confirmed arguments]
    T -->|Registered SQL| K
    T -->|New SQL required| N[LLM function calling<br/>SQL, argument definitions and values]
    K -->|Missing arguments| L[LLM function calling<br/>extract missing arguments]
    K -->|Arguments confirmed| Q[Queue ready work<br/>max_concurrent_queries]
    N --> V[Validate SQL and arguments]
    L --> V
    V --> Q
    Q --> E[Execute within the concurrency setting<br/>preserve dependency and write order]
    E --> R[Accumulate query results]
    R --> W[Collect queued work and running results]
    W -->|Ready work remains and a slot is available| Q
    W -->|Additional message received| S
    W -->|Queued and running work complete| C{Accumulated information sufficient?}
    C -->|Yes| F[Generate one combined final answer]
    C -->|No| H[Select next action]
    H -->|Additional function needed| D
    H -->|Explore related data| ER{Related link exists?}
    ER -->|Yes| NR{Related information needed?}
    NR -->|Yes| LK[Read linked lookup target]
    LK --> T
    ER -->|No| H
    NR -->|No| H
    H -->|Clarification or status response needed| F
    F --> G[Check current accumulated request state]
    G -->|New request content or pending work| S
    G -->|Ready| O[Send one final response]

    classDef jev fill:#d3a4ff,stroke:#6200cc,color:#203747;
    classDef llm fill:#98efa9,stroke:#006a28,color:#203747;
    classDef code fill:#f3f6f8,stroke:#8796a1,color:#203747;
    classDef data fill:#ffffff,stroke:#aab9c5,color:#203747;
    class D,T,C,H,ER,NR jev;
    class N,L,F llm;
    class S,A,P,K,V,Q,E,R,W,LK,G,O code;
    class FR,DB data;
```

- **Jev (purple):** function and schema selection, information sufficiency, and relationship decisions.
- **LLM (green):** missing argument extraction, new SQL generation, and final answer generation.
- **Code (gray):** immediate acknowledgements, concurrency control, queues, validation, and accumulated request state.

Additional messages and query results accumulate in the same active request. Required functions are selected without a count limit; only simultaneous queries are controlled by `max_concurrent_queries`. The accumulated request receives one combined final response.
