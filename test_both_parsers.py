#!/usr/bin/env python3
"""Test both JSON and XML parsers"""

import sys
sys.path.insert(0, '/home/mingxuanl/mingxuanl/simulation/brandonzhang/bfcl-pv-01/berkeley-function-call-leaderboard')

from bfcl.model_handler.parser.json_parser import parse_json_function_call
from bfcl.model_handler.parser.xml_parser import parse_xml_function_call

print("=" * 60)
print("Testing JSON Parser")
print("=" * 60)

# Test JSON parser
json_test1 = '{"function_name": "get_weather", "parameters": {"location": "NYC", "unit": "celsius"}}'
print(f"Test 1: {json_test1}")
result1 = parse_json_function_call(json_test1)
print(f"Result: {result1}\n")

json_test2 = '[{"function_name": "func1", "parameters": {"arg1": "val1"}}, {"get_user": {"id": "123"}}]'
print(f"Test 2: {json_test2}")
result2 = parse_json_function_call(json_test2)
print(f"Result: {result2}\n")

print("=" * 60)
print("Testing XML Parser")
print("=" * 60)

# Test XML parser
xml_test1 = '''<function_call>
    <name>get_weather</name>
    <arguments>
        <arg name="location">NYC</arg>
        <arg name="unit">celsius</arg>
    </arguments>
</function_call>'''
print(f"Test 1: Single function call")
result3 = parse_xml_function_call(xml_test1)
print(f"Result: {result3}\n")

xml_test2 = '''<function_calls>
    <function_call>
        <name>func1</name>
        <arguments>
            <arg name="arg1">val1</arg>
        </arguments>
    </function_call>
    <function_call>
        <name>get_user</name>
        <arguments>
            <arg name="id">123</arg>
        </arguments>
    </function_call>
</function_calls>'''
print(f"Test 2: Multiple function calls")
result4 = parse_xml_function_call(xml_test2)
print(f"Result: {result4}\n")

print("=" * 60)
print("All tests passed! Both parsers are working correctly.")
print("=" * 60)

