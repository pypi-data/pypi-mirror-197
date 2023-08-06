# colors_terminal

## Installation

`pip install Colors-Terminal`
## Usage

	from colors_terminal import Colors
	
	Colors.print("Hello, world!", color="pink", style="shadow")
	# Output: ERROR: Invalid color and style specified: 'pink' and 'shadow'

	Colors.print("Hello, world!", color="pink")
	# Output: ERROR: Invalid color specified: 'pink'

	Colors.print("Hello, world!", color="GREEN", style="BOLD")


## Update
We have fixed and improved the "print" function, now brings custom bugs and new more comfortable functions

## View
BOLD
DIM
ITALIC
UNDERLINE
BLINK
REVERSE
HIDDEN
    
BLACK
RED
GREEN
YELLOW
BLUE
MAGENTA
CYAN
WHITE
    
BG_BLACK
BG_RED
BG_GREEN
BG_YELLOW
BG_BLUE
BG_MAGENTA
BG_CYAN
BG_WHITE