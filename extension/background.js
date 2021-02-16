chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
	    urlo = tabs[0].url.replace(/\//g, 'µ');
	    // use `url` here inside the callback because it's asynchronous!
	    window.open("http://127.0.0.1:4000/" +urlo);
	});
});
