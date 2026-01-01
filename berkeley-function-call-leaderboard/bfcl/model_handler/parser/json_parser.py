import json


def parse_json_function_call(source_code):
    """
    Parse JSON-formatted function calls.
    
    Expected formats:
    1. Single call: {"function_name": "func", "parameters": {"param1": "value1"}}
    2. Multiple calls: [{"function_name": "func1", "parameters": {...}}, {"function_name": "func2", "parameters": {...}}]
    3. Simplified format: {"func_name": {"param1": "value1"}}
    
    Returns:
        List of dictionaries in format [{function_name: {param1: value1, ...}}]
    """
    try:
        parsed = json.loads(source_code)
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON: {str(e)}")
    
    result = []
    
    # Handle list of function calls
    if isinstance(parsed, list):
        for item in parsed:
            func_dict = _parse_single_json_call(item)
            if func_dict:
                result.append(func_dict)
    else:
        # Handle single function call
        func_dict = _parse_single_json_call(parsed)
        if func_dict:
            result.append(func_dict)
    
    return result if result else {}


def _parse_single_json_call(call_obj):
    """
    Parse a single JSON function call object.
    
    Args:
        call_obj: A dictionary representing a function call
        
    Returns:
        Dictionary in format {function_name: {param1: value1, ...}}
    """
    if not isinstance(call_obj, dict):
        raise Exception(f"Expected dictionary, got {type(call_obj)}")
    
    # Format 1: {"function_name": "func", "parameters": {...}}
    if "function_name" in call_obj and "parameters" in call_obj:
        func_name = call_obj["function_name"]
        params = call_obj["parameters"]
        if not isinstance(params, dict):
            raise Exception(f"Parameters must be a dictionary, got {type(params)}")
        return {func_name: params}
    
    # Format 2: {"name": "func", "arguments": {...}} (alternative naming)
    elif "name" in call_obj and "arguments" in call_obj:
        func_name = call_obj["name"]
        params = call_obj["arguments"]
        if not isinstance(params, dict):
            raise Exception(f"Arguments must be a dictionary, got {type(params)}")
        return {func_name: params}
    
    # Format 3: Simplified {"func_name": {"param1": "value1"}}
    # Assume single key-value where key is function name and value is parameters
    elif len(call_obj) == 1:
        func_name = list(call_obj.keys())[0]
        params = call_obj[func_name]
        if isinstance(params, dict):
            return {func_name: params}
        else:
            # Handle case where value is not a dict (no parameters)
            return {func_name: {}}
    
    else:
        raise Exception(f"Unrecognized JSON function call format: {call_obj}")


if __name__ == "__main__":
    # Test cases
    print("Testing JSON parser...")
    
    # Test 1: Standard format
    test1 = '{"function_name": "get_weather", "parameters": {"location": "New York", "unit": "celsius"}}'
    result1 = parse_json_function_call(test1)
    print(f"Test 1: {result1}")
    assert result1 == [{"get_weather": {"location": "New York", "unit": "celsius"}}], "Test 1 failed"
    
    # Test 2: Simplified format
    test2 = '{"get_weather": {"location": "Boston"}}'
    result2 = parse_json_function_call(test2)
    print(f"Test 2: {result2}")
    assert result2 == [{"get_weather": {"location": "Boston"}}], "Test 2 failed"
    
    # Test 3: Multiple calls
    test3 = '[{"function_name": "func1", "parameters": {"arg1": "val1"}}, {"function_name": "func2", "parameters": {"arg2": "val2"}}]'
    result3 = parse_json_function_call(test3)
    print(f"Test 3: {result3}")
    assert result3 == [{"func1": {"arg1": "val1"}}, {"func2": {"arg2": "val2"}}], "Test 3 failed"
    
    # Test 4: Alternative naming (name/arguments)
    test4 = '{"name": "send_email", "arguments": {"to": "user@example.com", "subject": "Hello"}}'
    result4 = parse_json_function_call(test4)
    print(f"Test 4: {result4}")
    assert result4 == [{"send_email": {"to": "user@example.com", "subject": "Hello"}}], "Test 4 failed"
    
    print("All tests passed!")


