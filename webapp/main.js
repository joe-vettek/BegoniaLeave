console.log("ok", 123)


window.onload = () => {
	document.querySelector("#select-all").addEventListener('click', (e) => {
		let selects = document.querySelector('.row-3>.box-in>.padding-2')
			.querySelectorAll('input');
		for (let s of selects) {
			s.checked = true;
		}
	});
	document.querySelector("#select-clear").addEventListener('click', (e) => {
		let selects = document.querySelector('.row-3>.box-in>.padding-2')
			.querySelectorAll('input');
		for (let s of selects) {
			s.checked = false;
		}
	});
	document.querySelector("#start").addEventListener('click', (e) => {
		let selects = document.querySelector('.row-3>.box-in>.padding-2')
			.querySelectorAll('input');

		let data = {
			"modules": []
		};
		for (let s of selects) {
			if (s.checked) data["modules"].push(s.id);
		}
		let state = document.querySelector("#start").innerHTML == "启动";
		let url = state ? '/api/connect' : "/api/disconnect";
		let _fetch = fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			})
			.then(response => {
				if (response.ok) {
					return response.json();
				} else {
					throw new Error(response.statusText);
				}
			})
			.then(function(response) {
				console.log(response)

				document.querySelector("#start").innerHTML = state ? "停止" : "启动";
				if (state)
					clearLog();
			}).catch((e) => {
				console.log(e)
			});
	})

	var myTarget = setInterval(function() {
		fetch('/api/log')
			.then(response => {
				if (response.ok) {
					return response.json();
				} else {
					throw new Error(response.statusText);
				}
			})
			.then((log) => {
				appendLog(log)
			}).catch((e) => {
				console.log(e)
			});
	}, 1000);

}

function clearLog() {
	document.querySelector("#log-area").innerHTML = "";
}

function appendLog(logs) {
	let sub_text = "";
	for (let l of logs) {
		let timetext = new Date(parseFloat(Object.keys(l).join('')) * 1000);
		let formattedDate =
			`${bn(timetext.getMonth() + 1)}-${bn(timetext.getDate())} ${bn(timetext.getHours())}:${bn(timetext.getMinutes())}:${bn(timetext.getSeconds())}`;
		let infog = Object.values(l).join('');
		sub_text += "<div>" + formattedDate + "</div><div>" + infog + "</div>";
	}
	if (sub_text.length > 0) {
		document.querySelector("#log-area").innerHTML += sub_text;
		document.querySelector("#log-area").scroll(0, document.querySelector("#log-area").scrollHeight);
	}
}

function bn(i) {
	return (i + "").padStart(2, "0");
}