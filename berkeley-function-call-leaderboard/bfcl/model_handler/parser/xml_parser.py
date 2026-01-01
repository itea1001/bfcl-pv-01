import xml.etree.ElementTree as ET


def parse_xml_function_call(source_code):
    """
    Parse XML formatted function calls.
    Expected format:
    <function_call>
        <name>function_name</name>
        <arguments>
            <arg name="param1">value1</arg>
            <arg name="param2">value2</arg>
        </arguments>
    </function_call>
    
    Or for multiple function calls:
    <function_calls>
        <function_call>
            <name>function_name1</name>
            <arguments>
                <arg name="param1">value1</arg>
            </arguments>
        </function_call>
        <function_call>
            <name>function_name2</name>
            <arguments>
                <arg name="param2">value2</arg>
            </arguments>
        </function_call>
    </function_calls>
    """
    try:
        # Try to parse the XML
        root = ET.fromstring(source_code)
    except ET.ParseError as e:
        raise Exception(f"Error parsing XML: {e}")
    
    def parse_single_call(call_element):
        """Parse a single function call element."""
        function_name = None
        arguments = {}
        
        for child in call_element:
            if child.tag == "name":
                function_name = child.text.strip() if child.text else ""
            elif child.tag == "arguments":
                # Parse arguments
                for arg in child:
                    if arg.tag == "arg":
                        arg_name = arg.get("name")
                        arg_value = arg.text.strip() if arg.text else ""
                        
                        # Try to convert to appropriate type
                        arg_value = convert_value(arg_value)
                        
                        if arg_name:
                            # Named argument
                            if arg_name in arguments:
                                raise Exception(
                                    "Error: Multiple arguments with the same name are not supported."
                                )
                            arguments[arg_name] = arg_value
                        else:
                            # Unnamed argument (use None as key)
                            if None in arguments:
                                if not isinstance(arguments[None], list):
                                    arguments[None] = [arguments[None]]
                                arguments[None].append(arg_value)
                            else:
                                arguments[None] = arg_value
        
        if not function_name:
            raise Exception("Error: Function name not found in XML.")
        
        return {function_name: arguments}
    
    def convert_value(value_str):
        """Convert string value to appropriate Python type."""
        # Try to parse as boolean
        if value_str.lower() == "true":
            return True
        elif value_str.lower() == "false":
            return False
        
        # Try to parse as number
        try:
            if "." in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass
        
        # Return as string
        return value_str
    
    # Check if root is a single call or multiple calls
    if root.tag == "function_call":
        # Single function call
        return [parse_single_call(root)]
    elif root.tag == "function_calls":
        # Multiple function calls
        result = []
        for call_element in root:
            if call_element.tag == "function_call":
                result.append(parse_single_call(call_element))
        return result
    else:
        raise Exception(f"Error: Unexpected root element '{root.tag}'. Expected 'function_call' or 'function_calls'.")

