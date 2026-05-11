def select_size(context: dict) -> str:
    if context.get("strategy"):
        return "small"
    return "large"
