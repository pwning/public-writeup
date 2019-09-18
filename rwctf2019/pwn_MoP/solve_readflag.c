#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

long long stack[100];
int stack_pointer = 0;

void goterror(const char* t) {
  perror(t);
}

static int
start_subprocess(char * command[], int *pid, int *infd, int *outfd)
{
    int p1[2], p2[2];

    if (!pid || !infd || !outfd)
        return 0;

    if (pipe(p1) == -1)
        goto err_pipe1;
    if (pipe(p2) == -1)
        goto err_pipe2;
    if ((*pid = fork()) == -1)
        goto err_fork;

    if (*pid) {
        /* Parent process. */
        *infd = p1[1];
        *outfd = p2[0];
        close(p1[0]);
        close(p2[1]);
        return 1;
    } else {
        /* Child process. */
        dup2(p1[0], 0);
        dup2(p2[1], 1);
        close(p1[0]);
        close(p1[1]);
        close(p2[0]);
        close(p2[1]);
        execvp(*command, command);
        /* Error occured. */
        fprintf(stderr, "error running %s: %s", *command, strerror(errno));
        abort();
    }

err_fork:
    close(p2[1]);
    close(p2[0]);
err_pipe2:
    close(p1[1]);
    close(p1[0]);
err_pipe1:
    return 0;
}

int seed;

int exp_rand()
{
  int v0; // eax@1

  ++seed;
  v0 = time(0LL);
  srand(v0 + seed * seed);
  return (rand() % 2);
}

int randval[4];
int signs[4];

void gen_str(char* dst) {
  randval[0] = exp_rand();
  randval[1] = exp_rand();
  randval[2] = exp_rand();
  randval[3] = exp_rand();
  signs[0] = (randval[0] == 1) ? -1 : 1;
  signs[1] = (randval[1] == 1) ? -1 : 1;
  signs[2] = (randval[2] == 1) ? -1 : 1;
  signs[3] = (randval[3] == 1) ? -1 : 1;
}

long long readnum(int infd) {
  long long sign = 1;
  char x;
  long long val = 0;
  read(infd, &x, 1);
  if ( x == '-' ) {
    sign = -1;
    read(infd, &x, 1);
  }
  while ( x != ')' ) {
    val *= 10;
    val += (x - '0');
    read(infd, &x, 1);
  }
  return val * sign;
}

int main() {
  char fmtstr[1000];
  gen_str(fmtstr);


  int pid, infd, outfd;
  char *cmd[2];
  cmd[0] = "/readflag";
  cmd[1] = 0;
  start_subprocess(cmd, &pid, &outfd, &infd);

  char buf1[1000];
  char buf[1000];

  read(infd, buf1, strlen("Solve the easy challenge first\n"));

  long long a, b, c, d, e;

  read(infd, buf1, strlen("((((("));
  a = readnum(infd);
  read(infd, buf1, strlen("+("));
  b = signs[0] * readnum(infd);
  read(infd, buf1, strlen(")+("));
  c = signs[1] * readnum(infd);
  read(infd, buf1, strlen(")+("));
  d = signs[2] * readnum(infd);
  read(infd, buf1, strlen(")+("));
  e = signs[3] * readnum(infd);

  long long v = a + b + c + d + e;
  char v_str[1000];
  sprintf(v_str, "%lld\n", v);

  write(outfd, v_str, strlen(v_str));
  read(infd, buf1, 1000);
  puts(buf1);
  read(infd, buf1, 1000);
  puts(buf1);
  read(infd, buf1, 1000);
  puts(buf1);

  return 0;
}
