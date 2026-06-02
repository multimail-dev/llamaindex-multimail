"""Example: Email assistant agent using LlamaIndex + MultiMail."""

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llamaindex_multimail import MultiMailToolSpec

# Create tool spec and convert to LlamaIndex tools
tool_spec = MultiMailToolSpec(api_key="MULTIMAIL_API_KEY")
tools = tool_spec.to_tool_list()

# Create a ReAct agent
llm = OpenAI(model="gpt-4o")
agent = ReActAgent.from_tools(
    tools,
    llm=llm,
    verbose=True,
    system_prompt=(
        "You are an email assistant. Use the MultiMail tools to help the user "
        "manage their email. The mailbox uses gated_send mode, so outbound "
        "emails will be held for human approval before delivery."
    ),
)

# Run the agent
response = agent.chat(
    "Check mailbox 'YOUR_MAILBOX_ID' for new emails and summarize them."
)
print(response)
