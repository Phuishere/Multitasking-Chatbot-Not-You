import re

def add_only_flags(text: str, command_string: str, colors: list[str] | None = None) -> str:
    """
    Insert 'only' into command_string based on occurrences in the original text.

    Parameters:
    - text: Original text string to check for 'only' usage (case-insensitive).
    - command_string: Semicolon-separated commands in the form "action,color".
                      E.g., "on,all;off,green".
    - colors: Optional list of colors to consider. If provided, only these colors will be checked;
              if None, any color in the command_string will be processed.

    Returns:
    - A semicolon-separated command string where 'only' is inserted as "action,only,color"
      if the pattern "<action> only <color>" appears in the text; otherwise retains "action,color".
    """
    text_lower = text.lower()
    commands = command_string.split(';')
    result_commands = []

    for cmd in commands:
        parts = [p.strip() for p in cmd.split(',')]
        # Expect exactly ["action", "color"]
        if len(parts) != 2:
            # Leave unchanged if format is unexpected
            result_commands.append(cmd)
            continue

        action, color = parts
        # If colors list is given, skip colors not in list
        if colors is not None and color not in colors:
            result_commands.append(cmd)
            continue

        # Build regex to find "<action> only <color>", optionally preceded by "turn "
        # Use word boundaries to avoid partial matches.
        # e.g., matches "turn off only red" or "off only red"
        pattern = re.compile(
            r'\b(?:turn\s+)?' + re.escape(action) + r'\s+only\s+' + re.escape(color) + r'\b',
            re.IGNORECASE
        )

        if pattern.search(text_lower):
            result_commands.append(f"{action},only,{color}")
        else:
            result_commands.append(cmd)

    return ";".join(result_commands)

if __name__ == "__main__":
    '''
    In this example, "on,yellow" matches "turn on only yellow" → "on,only,yellow"
    The first "off,green" might not match unless "off only green" appears before it.
    The second "off,green" matches "turn off only green" → "off,only,green"
    "blink,red" stays as "blink,red" unless text has "blink only red".
    '''
    
    # Suppose we already built a command string without 'only':
    example_text = "Please turn on only yellow lights, then off green, but later blink only red. Then blink all"
    example_commands = "on,yellow;off,green;blink,red;blink,all;"
    
    # Define the colors you care about:
    colors = ['red', 'green', 'yellow']

    updated = add_only_flags(example_text, example_commands, colors=colors)
    print("Original commands: ", example_commands)
    print("After adding 'only' flags:", updated)