#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>

int main(int argc, char **argv) {
  int dir_fd = open("/", O_RDONLY | O_DIRECTORY);

  struct sockaddr_un addr = {0};
  int sock = socket(AF_UNIX, SOCK_STREAM, 0);
  addr.sun_family = AF_UNIX;
  strcpy(addr.sun_path, "./sock");

  connect(sock, (struct sockaddr *) &addr, sizeof(addr));

  struct msghdr msg = {0};
  char control_buffer[CMSG_SPACE(sizeof(int))];
  msg.msg_control = control_buffer;
  msg.msg_controllen = sizeof(control_buffer);

  char c = 0xcc;
  struct iovec iov = { &c, sizeof(c) };
  msg.msg_iov = &iov;
  msg.msg_iovlen = 1;

  struct cmsghdr* cmsg = CMSG_FIRSTHDR(&msg);
  cmsg->cmsg_level = SOL_SOCKET;
  cmsg->cmsg_type = SCM_RIGHTS;
  cmsg->cmsg_len = CMSG_LEN(sizeof(int));
  *(int *) CMSG_DATA(cmsg) = dir_fd;

  sendmsg(sock, &msg, 0);
  return 0;
}
