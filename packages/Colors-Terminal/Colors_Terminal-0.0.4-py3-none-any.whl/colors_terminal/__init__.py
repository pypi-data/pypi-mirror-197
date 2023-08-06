class Colors:
    # Define ANSI escape codes for various text styles and colors
    # Define constants for different text styles and colors using ANSI escape codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @staticmethod
    def print(text, color="", style=""):
        # Check if the color and style are valid
        valid_colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        valid_styles = ['bold', 'dim', 'italic', 'underline', 'blink', 'reverse', 'hidden']
        if color.lower() not in valid_colors and (style is None or style.lower() not in valid_styles) and style != "":
            # Print an error message if the specified color and style are invalid
            print(f"{Colors.RED}{Colors.BOLD}ERROR: Invalid color and style specified: '{color}' and '{style}'{Colors.RESET}")
            return
        elif color.lower() not in valid_colors:
            # Print an error message if the specified color is invalid
            print(f"{Colors.RED}{Colors.BOLD}ERROR: Invalid color specified: '{color}'{Colors.RESET}")
            return
        elif (style is not None and style.lower() not in valid_styles) and style != "":
            # Print an error message if the specified style is invalid
            print(f"{Colors.RED}{Colors.BOLD}ERROR: Invalid style specified: '{style}'{Colors.RESET}")
            return

        # Attempt to get the ANSI escape code for the specified color by name
        try:
            color_code = getattr(Colors, color)
        except AttributeError:
            # If the specified color doesn't exist, raise a custom exception with a suggestion for a similar color (if available)
            if color.upper() in dir(Colors):
                print(f'{Colors.RED}{Colors.BOLD}ERROR: Invalid color specified: "{color}" (did you mean "{color.upper()}"?) {Colors.RESET}')
            else:
                print(f'{Colors.RED}{Colors.BOLD}ERROR: Invalid color specified: "{color}"{Colors.RESET}')
            return
        
        # Get the ANSI escape code for the specified style (if one was specified), or leave it blank if not
        if style is None or style == "":
            style_code = ""
        else:
            try:
                style_code = getattr(Colors, style)
            except AttributeError:
                # If the specified style doesn't exist, raise a custom exception with a suggestion for a similar style (if available)
                if style.upper() in dir(Colors):
                    print(f'{Colors.RED}{Colors.BOLD}ERROR: Invalid style specified: "{style}" (did you mean "{style.upper()}"?) {Colors.RESET}')
                else:
                    print(f'{Colors.RED}{Colors.BOLD}ERROR: Invalid style specified: "{style}"{Colors.RESET}')
                return

        # Print the text with the specified color and style, and then reset the color back to the default value at the end
        print(f"{style_code}{color_code}{text}{Colors.RESET}")
# Copyright © 2023 xXBlackDev9010Xx