# Infinite Agent

A domain-independent agent architecture for function calling, relational database retrieval, and conversations that accumulate requests while work is running.

**Status:** architecture and reproducible document tooling. The agent runtime, model adapters, database connectors, and delivery adapters are still to be implemented.

## How it works

1. Acknowledge every received message immediately with a short template.
2. Add follow-up requests to the same active request, preserving earlier requirements, results, and running calls.
3. Select all functions needed to fulfill the accumulated request. Function selection has no fixed count limit.
4. Run ready queries through a queue controlled by `max_concurrent_queries`. Dependencies and writes retain their required order.
5. Reuse confirmed arguments and registered SQL. Use LLM function calling for missing arguments or new SQL, then validate before execution.
6. Accumulate results, resolve remaining work, and assess whether the full request is ready for a response.
7. Generate one combined answer. Check the request version and delivery state before committing one logical final response.

Jev is an optional decision-router adapter for categorical and binary decisions. LLMs handle argument extraction, SQL generation, interpretation when needed, and answer drafting. Code manages execution, queues, request state, validation, and delivery.

## Documents

- [Architecture and state model](docs/architecture.md)
- [Career-domain HTML example](docs/examples/career/ontology-chat-plan.html)
- [Career-domain PDF example](docs/examples/career/ontology-chat-plan.pdf)

The career example illustrates one application of the architecture. Function registries, schemas, relation links, model providers, and delivery channels are intended to be replaceable across domains.

The example uses public job and company facts; résumé retrieval is a labeled scenario assumption. Document generation does not call model APIs or connect to production databases.

## Build and preview the documents

Prerequisites: Node.js 20.16 or later, npm, Python 3, and a Korean-capable Noto Sans CJK font.

```sh
npm install
npx playwright install chromium
npm run docs:build
npm run docs:serve
```

Open <http://127.0.0.1:8848/examples/career/ontology-chat-plan.html> for the local preview. These commands build and serve the documentation; they do not start an agent service.

An existing Chrome installation can be selected with `CHROME_PATH` instead of installing Playwright's Chromium. After editing the document sources, run `npm run docs:check` to verify the layout. Check outputs are written to `.artifacts/`.

## Implementation boundaries

The runtime should expose adapters for decision routing, LLM function calling, SQL validation and execution, state persistence, and message delivery. Database access and side effects must follow each registered function's execution contract.

[config.example.json](config.example.json) shows the proposed concurrency setting. It is an example contract for the future runtime.

One logical final response is recorded per active request. Reliable delivery across retries requires stable response identifiers and duplicate suppression in the delivery adapter.
