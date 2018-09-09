## pysandbox - Miscellaneous Challenge - Writeup by Robert Xiao (@nneonneo)

### Description

We are provided with the source code to a simple Python sandbox and asked to escape it. The sandbox takes a piece of Python code as input, parses it to an AST, and walks over the AST. If it finds any banned constructs (function calls and attribute accesses) it rejects your input; otherwise, it runs the code using `eval`.

### Solution

The AST walker is very simple - for each node, it checks if the node is allowed, and then visits a specified list of the node's attributes. Critically, it is missing some attributes for certain constructs, meaning that those attributes can contain arbitrary code that won't be visited or checked by the AST walker.

Specifically, it's missing `args` on the `Lambda` construct, meaning that the arguments of a `lambda` function can contain arbitrary unchecked code. Arguments can have default values which are evaluated at the moment the `lambda` is defined, so we can use that to build the exploit:

    lambda x=__import__('os').system('cat flag'): 0

There are two levels to this problem, but the second level **also** fails to ban Lambda args, so the exact same exploit works there. Thus, we get both flags easily:

    TWCTF{go_to_next_challenge_running_on_port_30002}
    TWCTF{baby_sandb0x_escape_with_pythons}
