# llamaindex-multimail

LlamaIndex tools for [MultiMail](https://multimail.dev) -- give your LlamaIndex agents email capabilities with graduated human oversight.

## Installation

```bash
pip install llamaindex-multimail
```

## Quick Start

```python
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llamaindex_multimail import MultiMailToolSpec

# Create tools from your API key
tool_spec = MultiMailToolSpec(api_key="MULTIMAIL_API_KEY")
tools = tool_spec.to_tool_list()

# Create agent
llm = OpenAI(model="gpt-4o")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

# Run
response = agent.chat("Check mailbox 'mbx_123' for new emails")
print(response)
```

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send an email (held for approval if gated) |
| `check_inbox` | List recent emails in a mailbox |
| `read_email` | Read the full content of an email |
| `reply_email` | Reply to an existing email thread |
| `search_contacts` | Search contacts by name or email |
| `list_pending` | List emails awaiting human approval |
| `decide_email` | Approve or reject a pending email |
| `get_thread` | Get all emails in a conversation |
| `tag_email` | Add tags to an email for classification |

This toolkit complements MultiMail's 38 MCP tools with LlamaIndex-native wrappers for common email workflows.

## Compliance

MultiMail handles regulatory compliance at the infrastructure layer — no SDK-side code changes needed:

- **EU AI Act Article 50**: Every AI-sent email includes a cryptographically signed `ai_generated` disclosure in the `X-MultiMail-Identity` header
- **US State Laws**: Maine, New York, California, Illinois — AI disclosure built into email delivery
- **CAN-SPAM**: Unsubscribe headers and physical address footers on all outbound email
- **Formally Verified**: Lean 4 proofs of identity header tamper evidence

MultiMail handles EU AI Act Article 50 compliance at the infrastructure layer. Every AI-sent email includes signed `ai_generated` disclosure automatically.

See [multimail.dev/use-cases/eu-ai-act-email-compliance](https://multimail.dev/use-cases/eu-ai-act-email-compliance) for details.

## Oversight Modes

MultiMail supports graduated oversight so your agent doesn't send unsupervised email:

- **`gated_all`** -- Agent drafts, human approves everything
- **`gated_send`** -- Agent reads freely, human approves outbound *(default)*
- **`monitored`** -- Agent sends, human can review after
- **`autonomous`** -- Full agent control

When a mailbox uses gated oversight, `send_email` returns `pending_send_approval` and the email waits for human review. The agent can check status with `list_pending`.

## Using with Other LlamaIndex Patterns

The `MultiMailToolSpec` follows the standard LlamaIndex `BaseToolSpec` pattern, so it works with any agent framework that accepts LlamaIndex tools:

```python
from llamaindex_multimail import MultiMailToolSpec

spec = MultiMailToolSpec(api_key="MULTIMAIL_API_KEY")

# Get all tools
tools = spec.to_tool_list()

# Or get a specific tool
send_tool = spec.to_tool_list(func_to_metadata_mapping={
    "send_email": {"name": "send_email", "description": "Send an email"},
})
```

## Links

- [MultiMail](https://multimail.dev) -- Homepage & docs
- [multimail](https://pypi.org/project/multimail/) -- Base Python SDK
- [langchain-multimail](https://pypi.org/project/langchain-multimail/) -- LangChain integration
- [MCP Server](https://www.npmjs.com/package/@multimail/mcp-server) -- For Claude, Cursor, and other MCP clients
