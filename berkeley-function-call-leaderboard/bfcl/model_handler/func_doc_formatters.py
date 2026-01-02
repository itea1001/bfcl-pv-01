"""
Function documentation formatters for converting JSON function docs to different formats.
"""
import json


def format_func_doc_as_json(functions):
    """Format function docs as JSON (default format)."""
    return json.dumps(functions, indent=2)


def format_func_doc_as_python(functions):
    """Format function docs as Python function signatures with docstrings."""
    result = []
    for func in functions:
        name = func["name"]
        desc = func["description"]
        params = func["parameters"]["properties"]
        required = func["parameters"].get("required", [])
        
        # Build function signature
        param_strs = []
        for param_name, param_info in params.items():
            param_type = param_info.get("type", "any")
            # Convert JSON types to Python types
            type_map = {
                "string": "str",
                "integer": "int",
                "number": "float",
                "boolean": "bool",
                "array": "list",
                "object": "dict"
            }
            py_type = type_map.get(param_type, param_type)
            
            if param_name in required:
                param_strs.append(f"{param_name}: {py_type}")
            else:
                param_strs.append(f"{param_name}: {py_type} = None")
        
        signature = f"def {name}({', '.join(param_strs)}):"
        
        # Build docstring
        docstring_parts = [f'    """{desc}']
        docstring_parts.append("\n    Args:")
        for param_name, param_info in params.items():
            param_desc = param_info.get("description", "No description")
            param_type = param_info.get("type", "any")
            docstring_parts.append(f"        {param_name} ({param_type}): {param_desc}")
        docstring_parts.append('    """')
        
        result.append(signature + "\n" + "\n".join(docstring_parts))
    
    return "\n\n".join(result)


def format_func_doc_as_xml(functions):
    """Format function docs as XML."""
    result = ["<functions>"]
    for func in functions:
        result.append("  <function>")
        result.append(f"    <name>{func['name']}</name>")
        result.append(f"    <description>{func['description']}</description>")
        result.append("    <parameters>")
        
        params = func["parameters"]["properties"]
        required = func["parameters"].get("required", [])
        
        for param_name, param_info in params.items():
            param_type = param_info.get("type", "string")
            param_desc = param_info.get("description", "")
            is_required = param_name in required
            
            result.append(f'      <parameter name="{param_name}" type="{param_type}" required="{str(is_required).lower()}">')
            result.append(f"        <description>{param_desc}</description>")
            result.append("      </parameter>")
        
        result.append("    </parameters>")
        result.append("  </function>")
    result.append("</functions>")
    
    return "\n".join(result)


def format_func_doc(functions, doc_fmt="json"):
    """
    Format function documentation according to specified format.
    
    Args:
        functions: List of function definitions in JSON format
        doc_fmt: Format to use ('json', 'python', or 'xml')
    
    Returns:
        Formatted function documentation string
    """
    if doc_fmt == "python":
        return format_func_doc_as_python(functions)
    elif doc_fmt == "xml":
        return format_func_doc_as_xml(functions)
    else:  # json or default
        return format_func_doc_as_json(functions)

