#include <stdio.h>
#include <stdlib.h>

int readCards(long long *deck) {
	int i;
	for (i = 0; i < 52; i++) {
		long long a;
		scanf ("%lld", &a);
		if (a == 0) return i;
		deck[i] = a;
	}
	return i;
}

void shuffle(long long *deck, int size) {
	int i;
	for (i = 0; i < size; i++) {
		long long val = deck[i];
		if (val < 0ll) {
			val = -val;
		}

    // swap deck[deck[i] % size] with deck[(i+1) % size)]
		long long temp = deck[val % size];
		deck[val % size] = deck[(i + 1) % size];
		deck[(i + 1) % size] = temp;
	}
}

int playGame(long long *deck, int size) {
	int i, j;
	long long sorted[52];
	int ind[52];
	int invInd[52];

	int played[52];
	int myS = 0;
	int theirS = 0;
	for (i = 0; i < size; i++) {
		sorted[i] = deck[i];
		invInd[i] = i;
		played[i] = 0;
	}

  //sort them
	for (i = 0; i < size; i++) {
		for (j = i + 1; j < size; j++) {
			if (sorted[i] > sorted[j]) {
				long long temp = sorted[i];
				sorted[i] = sorted[j];
				sorted[j] = temp;

				temp = invInd[i];
				invInd[i] = invInd[j];
				invInd[j] = temp;
			}
		}
	}
	for (i = 0; i < size; i++) {
		ind[invInd[i]] = i;
	}
	for (i = 0; i < size; i++) {
		printf ("Here are your cards left:\n");
		for (j = 0; j < size; j++) {
			if (played[j]) {
				printf ("(-) ");
			} else {
				printf ("%lld ", deck[j]);
			}
		}
		printf ("\nEnter the index of the card to play:\n");
		int toPl = 0;
		scanf ("%d", &toPl);
		while (toPl < 0 || toPl >= size || played[toPl]) {
			printf ("Bad card, silly\n");
			scanf ("%d", &toPl);
		}
		long long theirC = deck[toPl];
		long long myC = sorted[(ind[toPl] + 1) % size];
		played[toPl] = 1;
		printf ("You played %lld, I played %lld\n", theirC, myC);
		if (theirC < myC) {
			printf ("I won!\n");
			myS++;
		} else if (theirC > myC) {
			printf ("You won!\n");
			theirS++;
		} else {
			printf ("It was a draw\n");
		}
	}
	printf ("You got %d, I got %d\n", theirS, myS);
	return theirS > myS;
}

void printFlag() {
	FILE *f = fopen("flag.txt", "r");
	char flag[0x100];
	fread(flag, 1, 0x100, f);
	printf ("Have a flag:\n");
	printf ("%s\n", flag);
}

void handleRequests() {
	long long deck[52];
	while(1) {
		printf ("Lets play a game!\n");
		printf ("Enter up to 52 cards (0 to stop):\n");
		int size = readCards(deck);
		if (size == 0) {
			printf ("You need at least 1 card!\n");
			continue;
		}
		shuffle(deck, size);
		int res = playGame(deck, size);
		if (res) {
			printf ("Congrats, you won!\n");
			printFlag();
		} else {
			printf ("You didn't win, try harder next time :)\n");
		}
	}
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	handleRequests();
	return 0;
}
