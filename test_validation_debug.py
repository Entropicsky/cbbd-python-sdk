#!/usr/bin/env python3

"""
Debug script for validation.
"""

import sys
from cbbd.exceptions import CBBDValidationError
from cbbd.utils.validation import validate_date

def test_invalid_date():
    """Test invalid date validation."""
    print("Testing invalid date validation...")
    try:
        validate_date("01/01/2023")
        print("FAILED: No exception raised for 01/01/2023")
    except CBBDValidationError as e:
        print(f"SUCCESS: Caught expected exception: {e}")
    except Exception as e:
        print(f"FAILED: Caught unexpected exception: {type(e).__name__}: {e}")

    try:
        validate_date("not a date")
        print("FAILED: No exception raised for 'not a date'")
    except CBBDValidationError as e:
        print(f"SUCCESS: Caught expected exception: {e}")
    except Exception as e:
        print(f"FAILED: Caught unexpected exception: {type(e).__name__}: {e}")

    print("Tests completed.")

if __name__ == "__main__":
    test_invalid_date()
    sys.exit(0) 