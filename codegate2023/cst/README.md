# CST - pwnable challenge

We are given an C++ x86\_64 Linux binary (with no PIE) that appears to
be a custom C compiler frontend built on LLVM. The binary is run via a
provided python wrapper which writes reads source code from us, verifies
that it doesn't contain any '#' characters (i.e. no C preprocessor
directives - note that trigraphs were also disabled), and runs the
compiler frontend on it, sending back its stderr and stdout.

## Reversing

When run on a C program, the binary dumps some information about its
functions, as well as constucts such as for/while loops, if statements,
and switch statements.

Searching for references to those strings in the binary, we see that the
binary contains a custom AST visitor class, `MyASTVisitor`. This class
builds up some objects tracking the C constructs which are dumped.
Reversing those functions, we recover the following class layout/methods
for those objects:

```cpp
class Block {
 public:
  virtual Block* clone();
  virtual void dump();
  virtual std::string getType() { return type; }
  virtual void setType(const std::string& new_type) { type = new_type; }
  virtual void setNotation(int size, const std::string& notation) {
    if (size <= 64) {
      strcpy(notation, notation.c_str());
    }
  }
  virtual void addEdges(const std::string& edge);

  char notation[64];
  std::string type;
  std::vector<std::string> edges;
};

class WhileBlock : public Block {
 public:
  std::string condition;
};

// similar types for `FunctionBlock`, `ForBlock`, `IfBlock`,
// `SwitchBlock`, `CaseBlock`

```

The `notation` field imediately stands out because it is char buffer
that is populated with `strcpy()`. Looking at where it is populated, we
see that it typically contains a string describing the line/column of a
block in the source code. However, it can sometimes be set to other
attacker-controlled values. For example, in
`MyASTVisitor::VisitWhileStmt()`, there is code that at a high level,
does:

```cpp
void MyASTVisitor::VisitWhileStmt(WhileStmt* while_stmt) {
  WhileBlock *while_block = new WhileBlock(/*type=*/"WhileBlock",
                                           /*notation=*/"");
  for (stmt : while_loop_body_statements) {
    ...
    if (call_expr = dyn_cast<CallExpr>(expr)) {
      std::string callee_str = ...;  // name of function being called
      std::string args_str = ...;    // text of the arguments to the call
      if (callee_str == "annotation") {
        size_t length = arg_str.size();
        if (arg_str.front() == '"') {
          for (int i = 1; i < arg_str.size(); ++i) {
            if (arg_str[i] == '"') {
              length = i - 1;
              break;
            }
          }
        }
        while_expr->setNotation(length, args_str);
      } else if (callee_str == "type" &&
                 args_str.size() <= 18) {
        while_expr->setType(args_str);
      }
    }
    ...
  }
}
```

This has a pretty obvious bug where the length computed by counting the
number of characters between the first pair of double quotes can be
significantly less than the size of `callee_str`. This allows us to
overflow the `notation` buffer by running the binary on code like:
```c
void test() {
  while (1) {
    annotation("""AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
  }
}
```

## Exploitation

Luckily, LLVM is willing to parse C source code with almost arbitrary
characters in string literals (including null bytes and unprintable
characters), and these characters make it through into the `args_str`
string above.

The general approach for exploitation is:
1. Arrange the memory layout so that some existing `WhileStmt` appears
   later in memory than the `WhileStmt` being populated in
   `VisitWhileStmt` (the exploit manipulates a heap this by creating a
   `WhileStmt` with a condition string of length `sizeof(WhileStmt)`.
   The code ends up cloning this `WhileStmt` and deleting the original
   `WhileStmt`, which frees the condition string for a `WhileStmt` to be
   allocated into).
2. Repeatedly trigger the `strcpy` overflow to corrupt memory beyond the
   current `WhileStmt`'s notation buffer. Since each `strcpy` will write
   exactly one null byte at the end, the exploit writes its payload in
   backwards order, requiring one `annotation()` call per null byte that
   needs to be written.
3. Use the overflow to overwrite `type_str`'s data pointer and capacity.
   This provides an arbitrary write (of up to 18 bytes, where the first
   and last byte are double quote characters).
4. Use the arbitrary write to write a fake vtable into BSS (as well as a
   command that we will eventually call `system()` on.
5. Use the overflow to overwrite an adjacent `WhileStmt`'s vtable to
   point to the fake vtable, as well as write a ROP payload. When that
   `WhileStmt`'s virtual `dump()` method is called, it calls into a fake
   vtable entry which pivots the stack to point at the `WhileStmt`
   object, and then executes the ROP payload.
6. The ROP payload computes the address of system and calls it on the
   command that was written into BSS.

See exploit.py for more details.
