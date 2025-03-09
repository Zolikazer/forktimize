import pytest

from model.alias_generator import to_camel


@pytest.mark.parametrize("input_string, expected_output", [
    ("hello_world", "helloWorld"),  # ✅ Standard snake_case
    ("this_is_a_test", "thisIsATest"),  # ✅ Multiple words
    ("word", "word"),  # ✅ Single word (no change)
    ("leading_underscore", "leadingUnderscore"),  # ✅ Handles normal words
    ("_leading_underscore", "LeadingUnderscore"),  # ✅ Leading underscore (edge case)
    ("trailing_underscore_", "trailingUnderscore"),  # ✅ Trailing underscore
    ("", ""),  # ✅ Empty string
    ("helloWorld", "helloWorld"),  # ✅ Already camelCase (no change)
    ("snake_case_test", "snakeCaseTest"),  # ✅ Another snake_case example
])
def test_to_camel(input_string, expected_output):
    """Test the to_camel function with various cases."""
    assert to_camel(input_string) == expected_output
