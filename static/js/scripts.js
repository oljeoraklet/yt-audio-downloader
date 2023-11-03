document
	.getElementById("downloadForm")
	.addEventListener("submit", function (e) {
		e.preventDefault();
		var url = document.getElementById("url").value;
		document.getElementById("loadingSpinner").style.display = "flex"; // Show loading spinner

		fetch("/process", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: "url=" + encodeURIComponent(url),
		})
			.then((response) => response.json())
			.then((data) => {
				document.getElementById("loadingSpinner").style.display = "none"; // Hide loading spinner
				document.getElementById("fileName").textContent = data.fileName;
				document.getElementById("downloadButton").href =
					"/download?fileName=" + encodeURIComponent(data.fileName);
				document.getElementById("downloadLink").style.display = "block";
			});
	});
