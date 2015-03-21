# bookstore (400pts)

## Description
```
Binary : http://binary.grayhash.com/7692931e710c1d805224c44ab97ddd52/bookstore
Server : 54.65.201.110
Port : TCP 31337
Flag Path : /home/bookstore/key
```

## Solution
This is a simple bookstore management service where a user can

- add a book
- update existing book
- view details on a selected book
- show the book list

We notice that there is a `login (sub_1495)` function that checks for the username and password. In this function, the service first reads a file (_/home/bookstore/famous\_saying.txt_) and prints out its content by calling `dump_file (sub_8d8)` function, where the argument is a path to the file to read. So, once we have a control over EIP, we can direct it to `dump_file` with the first argument pointing to the flag path (_/home/bookstore/key_) to print out the flag rather than getting a shell.

Since `bookstore` is a PIE binary, we first need to leak a useful pointer to calculate our offsets from. Then, we use an uninitialized stack variable (function pointer) to execute `dump_file` on the file path we control.

### Leaking memory
After some reversing, we know that the internal data structure that is being used to represent a book is as follows.

```
struct struc_book
{
  int id;
  int is_ebook;
  char name[20];
  int price;
  int stock;
  int print_desc;             // function pointer
  int has_free_shipping;
  int print_free_shipping;    // function pointer
  int max_download;
  int is_available;
  char description[300];
};
```
When creating a new book, in `create_book (sub_A07)`, the name and description of the book is properly null-terminated. However, in `modify_bookname (sub_EDA)`, the name of the book is updated using `strncpy` without properly null-terminating the string.

This vulnerability allows us to fill up the `name` field with a non-null-terminated string. `price` and `stock` field is integer fields without any limit or checks, so we can also make these to not contain any null bytes. What follows afterwards is a function pointer `print_desc`, which is normally set to `print_desc_fn (sub_9AD)`.

So, after creating a book and modifying its info with carefully crafted values for some of the fields, we can leak the function pointer by using its "4. Show item list" menu. From this, we can calculate the address of `dump_file` function.

### Exploiting uninitialized memory
Now that we have the address for our target function, we need to somehow redirect the control flow to it.

For that, we exploit the usage of uninitialized stack variable. In order to trigger this bug, we do the following.

1. Create a **non-Ebook** (aka, normal book).
   - Name and description can be anything.
2. Modify the book information for the book we just created.
   - Stock, price, and available can be anything.
   - **Set 0 for "Free Shipping"**.
   - Set name to be the flag path (for exploitation).
3. Modify the free shipping status.
   - **Set it to 1**.
   - (Only non-Ebook can change this status)
4. Go back to main menu & view the book detail

Note that in step 2, the service uses a temporary book object on the stack to fill in data and copies over to the book object pointer that is passsed in as an argument. By setting "Free Shipping" to 0, `print_free_shipping` function pointer in temporary book object is not initialized (then later gets copied over with whatever it is on the stack).

Usually, this isn't a problem because in "view book information" menu, it checks if the `has_free_shipping` flag is set and calls the `print_free_shipping` function only if the flag is set. However, it is possible to change this flag with `modify_free_shipping (sub_1098)` menu. Note that this function does not initialize the function pointer, but just simply changes the flag.

When we go back to the main menu and select to view the book detail, `print_book_info (sub_1395)` will check for `has_free_shipping` flag and gladly call the uninitialized function pointer :)

We control the value for this function pointer by "spraying" the stack with the address of `dump_file`. Spraying can be done using `modify_book_desc (sub_FB9)` menu. As we can see, `print_free_shipping` takes one argument, which is the name of the book. So by setting the name to the path we want to read and print, and overriding the function pointer with `&dump_file`,  `print_free_shipping_fn(bookname)` becomes `dump_file(path_we_control)`.

## Flag
```
but_1_h4t3_b00oooooooo00k_:(((
```