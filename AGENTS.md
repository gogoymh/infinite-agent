# Infinite Agent

## Scope

This repository currently contains architecture documentation and reproducible
career-example document sources. Describe implemented behavior separately from
planned agent runtime behavior.

## Architecture invariants

- Keep the core independent of a business domain and any model, chat channel,
  or database provider. Put domain-specific definitions in examples or adapters.
- Select every function required by a request. Limit concurrent queries through
  `max_concurrent_queries`, not by truncating the selected function list.
- Keep dependency ordering and write ordering separate from independent queries.
- Reuse validated arguments and registered SQL; use LLM Function Calling for
  unresolved arguments and new SQL definitions and values.
- Acknowledge every incoming message promptly. Merge additional messages into
  the active request and preserve completed and running queries.
- Collect queued and running work before assessing the accumulated requirements.
- Validate request version and delivery state before final output. Use a stable
  response identity and provider-supported idempotency for delivery retries.

## Documentation and validation

- Keep generic documentation in English and label domain examples explicitly.
- Keep diagram node numbers consistent across the overview and examples.
- Preserve SVG text as fill-only to keep exported PDF text clear.
- Run `npm run docs:check` after changing the example diagram or document sources.
- Do not commit production exports, user messages, credentials, private keys,
  local machine paths, or private database audit results.
- Use an AS IS / TO BE comparison with a labeled diagram or verified screenshot
  when writing pull request descriptions. Include relevant validation.
