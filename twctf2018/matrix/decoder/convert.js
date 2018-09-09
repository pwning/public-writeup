// Converts Weka's J48 tree output to Arduino code that can simply be dropped
// into index.py.

const fs = require("fs-extra");

// Returns a string consisting of d+1 tabs
function tab(d) {
	let ret = "";
	for (let i = 0; i <= d; i++) {
		ret += "\t";
	}
	return ret;
}

fs.readFile("weka.txt")
	.then((data) => {
		let content = "";

		// Read the data from the file, and trim it to only include the decision tree
		data = data.toString();
		data = data.split("------------------\n\n")[1];
		data = data.split("\n\nNumber of Leaves")[0];

		// Current tab depth
		let depth = 0;

		for (let line of data.split("\n")) {
			if (line == "") {
				continue;
			}

			// Split to determine decision depth
			let parts = line.split("|   ");

			// The condition is everything after the last "|   "
			let condition = parts.pop();

			// Use a regex to capture the important parts of the condition
			let matches = /^(.*) (>|<=) (-?\d+(?:\.\d+)?)(: (\d+))?/.exec(condition);
			console.log(matches);

			if (!matches) {
				// If our condition didn't match the format, freak out
				console.log(condition);
				throw "What?";
			}

			if (matches[2] == "<=") {
				// If we have a "less than or equal to" condition, we don't need to close any blocks; simply add the if
				content += `${tab(depth)}if ${matches[1]} <= ${matches[3]}:\n`;
			} else {
				// If we have a "greater than" condition, we may need to close one or more blocks
				let first = true;

				// Keep closing blocks until the depth matches the actual depth of this condition
				while (depth > parts.length) {
					depth--;
					if (!first) {
						content += "\n";
					}
					content += `${tab(depth)}`;
					first = false;
				}

				// Add the else corresponding to this greater-than condition
				content += `else:\n`;
			}

			// Update the depth
			depth++;

			if (matches[5]) {
				// If the line ended with ": name_here", then this is a leaf matching the "name_here" gesture
				content += `${tab(depth)}answer = ${matches[5]}\n`;
			}
		}

		// Keep closing blocks until there are no blocks left to close
		let first = true;

		while (depth > 0) {
			depth--;
			if (!first) {
				content += "\n";
			}
			content += `${tab(depth)}`;
			first = false;
		}

		// Write the model to the output file
		fs.writeFile("model.txt", content);
	})