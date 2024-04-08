console.log("ok", 123)


window.onload = () => {
	document.querySelector("#select-all").addEventListener('click', (e) => {
		let selects = document.querySelector('.row-3>.box-in>.padding-2')
			.querySelectorAll('input');
		for (let s of selects) {
			if (s.id != "battle-huangdian")
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


				if (state)
					clearLog();
			}).catch((e) => {
				console.log(e)
			});
	})

	var status = -1;
	var myTarget = setInterval(async function() {
		try {
			// 发起网络请求
			const response = await fetch('/api/status');

			if (status != 1) {
				document.querySelector(".status-bar").innerHTML =
					"<div style='color:#c4d7d6'>后台服务进程连接中</div>";
				document.querySelector(".status-bar").classList.remove('blinking');
			}
			status = 1;
		} catch (error) {
			// 捕获异常
			console.log('Connect error:');
			if (status != 0) {
				document.querySelector(".status-bar").innerHTML =
					"<div style='color:#30161c'>后台服务进程已断开</div>";
				document.querySelector(".status-bar").classList.add('blinking');
			}
			status = 0;
			// document.querySelector("#log-area").scroll(0, document.querySelector("#log-area").scrollHeight);
		}
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
		fetch('/api/status')
			.then(response => {
				if (response.ok) {
					return response.json();
				} else {
					throw new Error(response.statusText);
				}
			})
			.then((status) => {
				document.querySelector("#start").innerHTML = status["code"] == 200 ? "停止" : "启动";
			}).catch((e) => {
				console.log(e)
			});
	}, 1000);

	document.getElementById("openDialog").addEventListener("click", function() {
		fetch("/api/config")
			.then(response => {
				if (response.ok) {
					document.getElementById("dialogOverlay").style.display = "block";
					return response.json();
				} else {
					alert('后台服务似乎未启动。');
				}
			})
			.then((json) => {
				document.getElementById("port").value = json["port"];
			})
	});

	document.getElementById("closeDialog").addEventListener("click", function() {
		document.getElementById("dialogOverlay").style.display = "none";
	});

	document.getElementById("saveButton").addEventListener("click", function() {

		fetch("/api/config", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"config": {
					"port": parseInt(document.getElementById("port").value)
				}
			})
		}).then(response => {
			if (response.ok) {
				document.getElementById("dialogOverlay").style.display = "none";
			} else {
				alert('后台服务似乎未启动。');
			}
		});
	});

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