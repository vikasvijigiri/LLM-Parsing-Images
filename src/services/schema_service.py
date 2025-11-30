import json

def extract_schema_from_gt(gt_list):
    """
    Extract schema from a ground-truth JSON list.

    Args:
        gt_list (list): List of ground-truth JSON objects (dicts)

    Returns:
        list: List of schema dicts with values replaced by type placeholders
    """

    def _extract_schema(obj):
        if isinstance(obj, dict):
            return {k: _extract_schema(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            if len(obj) == 0:
                return []  # empty list
            # recursively extract schema from first element
            return [_extract_schema(obj[0])]
        else:
            return "string"  # default placeholder for value

    return [_extract_schema(item) for item in gt_list]
