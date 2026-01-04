#!/usr/bin/env python3
"""Test the tagged format parsing."""

import sys
sys.path.insert(0, '/home/mingxuanl/mingxuanl/simulation/brandonzhang/bfcl-pv-01/berkeley-function-call-leaderboard')

from bfcl.model_handler.utils import ast_parse, strip_tool_call_tags

# Test 1: Strip tool_call tags
print("Test 1: Stripping tool_call tags")
tagged_input = "<tool_call>test content</tool_call>"
result = strip_tool_call_tags(tagged_input)
print(f"  Input: {tagged_input}")
print(f"  Output: {result}")
assert result == "test content", f"Expected 'test content', got '{result}'"

# Test 2: Strip with whitespace
print("\nTest 2: Stripping with whitespace")
tagged_input = "  <tool_call>  test content  </tool_call>  "
result = strip_tool_call_tags(tagged_input)
print(f"  Input: '{tagged_input}'")
print(f"  Output: '{result}'")
assert result == "test content", f"Expected 'test content', got '{result}'"

# Test 3: No tags
print("\nTest 3: No tags (passthrough)")
plain_input = "test content"
result = strip_tool_call_tags(plain_input)
print(f"  Input: {plain_input}")
print(f"  Output: {result}")
assert result == "test content", f"Expected 'test content', got '{result}'"

# Test 4: Python tagged format
print("\nTest 4: Python tagged format parsing")
tagged_python = '<tool_call>[get_weather(location="New York")]</tool_call>'
result = ast_parse(tagged_python, language="PythonTagged")
print(f"  Input: {tagged_python}")
print(f"  Output: {result}")
assert len(result) == 1, f"Expected 1 function call, got {len(result)}"
assert 'get_weather' in result[0], f"Expected 'get_weather' in result, got {result}"

# Test 5: JSON tagged format
print("\nTest 5: JSON tagged format parsing")
tagged_json = '<tool_call>{"function_name": "get_weather", "parameters": {"location": "Boston"}}</tool_call>'
result = ast_parse(tagged_json, language="JSONTagged")
print(f"  Input: {tagged_json}")
print(f"  Output: {result}")
assert len(result) == 1, f"Expected 1 function call, got {len(result)}"
assert 'get_weather' in result[0], f"Expected 'get_weather' in result, got {result}"

# Test 6: XML tagged format
print("\nTest 6: XML tagged format parsing")
tagged_xml = '''<tool_call>
<function_call>
    <name>get_weather</name>
    <arguments>
        <arg name="location">Seattle</arg>
    </arguments>
</function_call>
</tool_call>'''
result = ast_parse(tagged_xml, language="XMLTagged")
print(f"  Input: {tagged_xml[:50]}...")
print(f"  Output: {result}")
assert len(result) == 1, f"Expected 1 function call, got {len(result)}"
assert 'get_weather' in result[0], f"Expected 'get_weather' in result, got {result}"

print("\n✓ All tests passed!")

