# If you want to list all the tools called in the agent run
# Tools Called
tool_calls = [it for it in agent_result.new_items if isinstance(it, ToolCallItem)]
print("Tools called:")
for i, it in enumerate(tool_calls, 1):
    raw = it.raw_item
    name = getattr(raw, "name", getattr(raw, "tool_name", "unknown_tool"))
    args = getattr(raw, "arguments", getattr(raw, "input", None))
    print(f"{i}. {name}  args={args}")

# Tools Output
tool_outputs = [it for it in agent_result.new_items if isinstance(it, ToolCallOutputItem)]
print("\nTool outputs:")
for i, it in enumerate(tool_outputs, 1):
    raw = it.raw_item
    print(f"{i}. {it.output!r}")
