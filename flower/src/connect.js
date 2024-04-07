function timeoutFetch(timeout = 500) {

	return (url, option = {}) => {
		const controller = new AbortController()
		option.signal = controller.signal
		// 设置一个定时器，超时后调用abort方法结束当前请求
		const tid = setTimeout(() => {
			console.error(`Fetch timeout: ${
			     url}`)
			controller.abort()
		}, timeout)
		return fetch(url, option).finally(() => {
			clearTimeout(tid)
		})
	}
}

async function to_load() {
	let frame = document.querySelector('iframe');
	try {
		// await fetch(frame.src);
		await timeoutFetch(200)(frame.src);
		frame.classList.add('iframe');
	} catch (e) {
		frame.src = frame.src;
		console.log("尝试重载", new Date())
	}
	timeoutFetch();
}

function reloadFrame() {
	// setTimeout(to_load, 500);
	// 本身有超时时间，不必等待
	to_load();
}


async function start() {
	c = window.__TAURI__.shell.Command;

	command = new c('start-bridge-server', ['webapp.py']);
	command.on('close', data => {
		console.log(`command finished with code ${data.code} and signal ${data.signal}`)
	});
	command.on('error', error => console.error(`command error: "${error}"`));
	command.stdout.on('data', line => console.log(`command stdout: "${line}"`));
	command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

	const child = await command.spawn();
	console.log('pid:', child.pid);
};

async function stop() {
	c = window.__TAURI__.shell.Command

	command = new c('force-stop-bridge-server')
	command.on('close', data => {
		console.log(`command finished with code ${data.code} and signal ${data.signal}`)
	});
	command.on('error', error => console.error(`command error: "${error}"`));
	command.stdout.on('data', line => console.log(`command stdout: "${line}"`));
	command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

	const child = await command.spawn();
	console.log('pid:', child.pid);
};