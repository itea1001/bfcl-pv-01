# Failure Case Analysis: Prompt Variation Comparison

## Summary

XML format has significantly lower performance compared to Python and JSON, primarily due to **type inference errors** in the XML parser.

## Performance Comparison (parallel_multiple category)

- **Python**: 88.5% accuracy
- **JSON**: 76.5% accuracy  
- **XML**: 51.0% accuracy

## Main Issue: XML Type Inference

**83.7% of XML failures** in parallel_multiple are type-related errors.

### Example Failure

**Test**: `parallel_multiple_0`  
**Question**: "Find the sum of all the multiples of 3 and 5 between 1 and 1000."

**XML Model Output**:
```xml
<function_calls>
    <function_call>
        <name>math_toolkit.sum_of_multiples</name>
        <arguments>
            <arg name="lower_limit">1</arg>
            <arg name="upper_limit">1000</arg>
            <arg name="multiples">[3, 5]</arg>
        </arguments>
    </function_call>
</function_calls>
```

**Problem**:
- XML parser reads `<arg name="multiples">[3, 5]</arg>` as **string** `"[3, 5]"`
- Expected type is **array** `[3, 5]`
- Result: **FAIL**

**Why JSON/Python don't have this issue**:
- JSON natively supports typed data: `{"multiples": [3, 5]}` is parsed correctly as an array
- Python function syntax is explicit: `multiples=[3, 5]` is clearly an array

## Common XML Type Errors

1. **Array misidentified as string**: `[3, 5]` → `"[3, 5]"`
2. **Integer when float expected**: `7` → `7` (int) instead of `7.0` (float)
3. **Complex nested structures**: Objects/arrays inside arrays are especially problematic

## Error Distribution (parallel_multiple)

### XML Errors (98 total failures)
- `cannot_find_match`: 92 (mostly type errors)
- `decoder_failed`: 4
- `wrong_count`: 2

### JSON Errors (47 total failures)
- `cannot_find_match`: 45
- `wrong_count`: 2

**JSON has roughly half the failures of XML**, and most JSON failures are genuine model errors (wrong function calls, missing parameters) rather than parser issues.

## Recommendation

The XML parser needs improved type inference logic to:
1. Detect array literals `[...]` and parse them as arrays, not strings
2. Use function schema information to cast types appropriately (int vs float)
3. Handle nested complex types

