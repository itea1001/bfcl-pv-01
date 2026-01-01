#!/usr/bin/env python3
"""
Simple test script for the XML parser.
"""

from bfcl.model_handler.parser.xml_parser import parse_xml_function_call


def test_single_function_call():
    """Test parsing a single function call."""
    xml_input = """
    <function_call>
        <name>get_weather</name>
        <arguments>
            <arg name="location">New York</arg>
            <arg name="unit">celsius</arg>
        </arguments>
    </function_call>
    """
    
    result = parse_xml_function_call(xml_input)
    print("Test 1 - Single function call:")
    print(result)
    assert len(result) == 1
    assert "get_weather" in result[0]
    assert result[0]["get_weather"]["location"] == "New York"
    assert result[0]["get_weather"]["unit"] == "celsius"
    print("✓ Test 1 passed\n")


def test_multiple_function_calls():
    """Test parsing multiple function calls."""
    xml_input = """
    <function_calls>
        <function_call>
            <name>get_weather</name>
            <arguments>
                <arg name="location">New York</arg>
            </arguments>
        </function_call>
        <function_call>
            <name>send_email</name>
            <arguments>
                <arg name="to">user@example.com</arg>
                <arg name="subject">Weather Update</arg>
            </arguments>
        </function_call>
    </function_calls>
    """
    
    result = parse_xml_function_call(xml_input)
    print("Test 2 - Multiple function calls:")
    print(result)
    assert len(result) == 2
    assert "get_weather" in result[0]
    assert "send_email" in result[1]
    print("✓ Test 2 passed\n")


def test_type_conversion():
    """Test automatic type conversion."""
    xml_input = """
    <function_call>
        <name>calculate</name>
        <arguments>
            <arg name="value">42</arg>
            <arg name="multiplier">1.5</arg>
            <arg name="enabled">true</arg>
        </arguments>
    </function_call>
    """
    
    result = parse_xml_function_call(xml_input)
    print("Test 3 - Type conversion:")
    print(result)
    assert result[0]["calculate"]["value"] == 42
    assert result[0]["calculate"]["multiplier"] == 1.5
    assert result[0]["calculate"]["enabled"] is True
    print("✓ Test 3 passed\n")


if __name__ == "__main__":
    print("Running XML parser tests...\n")
    try:
        test_single_function_call()
        test_multiple_function_calls()
        test_type_conversion()
        print("All tests passed! ✓")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

