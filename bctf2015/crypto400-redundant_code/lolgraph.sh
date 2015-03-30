#!/bin/sh
# Solver for the redundant_code challenge. It's a totally straightforward
# character-by-character brute force, that uses `sdiff` to pick the input
# that generates output most similar to the target output.
#
# Run it from a script with the decompressed challenge files, and it will
# produce the flag. Be aware that there's a "444444444" in the flag.

score() {
  # Scores an input. Higher scores are worse.
  local MYTEMP=`mktemp -t lolgraph.XXXXXX`
  ./redundant-code "$1" | sdiff -H -w 20 ./code.pub - > "$MYTEMP"

  # The factor 20 here is used to strongly punish inputs for having lines
  # that don't match the target output. Without it, inputs that generate
  # bigger graphs will tend score better, even if they don't match well.
  printf '%d\t%s\n' $((`grep -ce '<' "$MYTEMP"` + 20 * `grep -ce '>' "$MYTEMP"`)) "$1"
  rm "$MYTEMP"
}

TEMPBASE=`mktemp -t lolgraph.XXXXX`
export FLAG='BCTF{r3cov3rable_flA9_f444444444r_y'
printf '\n\n\n'
while true; do
  # Test all the characters in parallel
  for C in q w e r t y u i o p l k j h g f d s a z x c v b n m 0 1 2 3 4 5 6 7 8 9 Q W E R T Y U I O P A S D F G H J K L Z X C V B N M _ '{' '}'; do
    { score "$FLAG""$C" > "$TEMPBASE""$C" & } 2> /dev/null
  done
  { wait; } 2> /dev/null

  # Pick the character with the lowest score, and print out the top three.
  # This is useful to see that there's a clear best next char; otherwise,
  # we'd know that the bruteforcer isn't really working.
  printf '\033[3A\033[K\n\033[K\n\033[K\n\033[3A' > /dev/stderr
  export FLAG="$(cat "$TEMPBASE"* | sort -n | grep '^[0-9]' | head -n 3 | tee -a /dev/stderr | head -n 1 | awk '{print $2}')"
  grep -sqEe '^0\s' "$TEMPBASE"* && break
done
printf '\033[3A\033[K\n\033[K\n\033[K\n\033[3A' > /dev/stderr
printf '%s\n' "$FLAG"
