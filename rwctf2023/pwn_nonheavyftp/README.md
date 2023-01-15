## [RWCTF 2023] NonHeavyFTP

The challenge is running the LightFTP v2.2 release binary without any modification.

#### Vulnerability

The way server uses `PFTPCONTEXT->FileName` leads to a race condition that allows accessing file outside the configured root path for the FTP server.

```c

void *list_thread(PFTPCONTEXT context)
{
    ...
            ret = list_sub(context->FileName, clientsocket, TLS_datasession, entry); // list the directory using the path saved in `context->FileName` array
    ...
}

int ftpLIST(PFTPCONTEXT context, const char *params)
{
    ...
    ftp_effective_path(context->RootDir, context->CurrentDir, params, sizeof(context->FileName), context->FileName); // calculate the effective path to list directory
    ...
        context->WorkerThreadValid = pthread_create(&tid, NULL, (void * (*)(void *))list_thread, context); 
    ...
}

int ftpUSER(PFTPCONTEXT context, const char *params)
{
    ...
    snprintf(context->FileName, sizeof(context->FileName), "331 User %s OK. Password required\r\n", params);
    ...
    /* Save login name to FileName for the next PASS command */
    strcpy(context->FileName, params); // copy the username to `context->FileName` array
    return 1;
}
```

In the above snippet, `ftpLIST` computes the effective path and saves it into `context->FileName`. Then a new thread is spawned which will use the effective path and transfer data over the data port. This handling in new thread can be raced by sending a `USER` command on the control port with the path we would like to access in file system. Since `ftpUSER` copies the username into `context->FileName` we can overwrite the path computed by `ftp_effective_path`.

Similar race condition exist in other commands that is handled in a separate thread and uses `FileName`.

This was used in our ([`exploit script`](exploit.py)) to retrieve the flag: `rwctf{race-c0nd1tion-1s-real1y_ha4d_pr0blem!!!}`.
