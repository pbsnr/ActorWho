chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
	    urlo = tabs[0].url.replace(/\//g, '(');
	    // use `url` here inside the callback because it's asynchronous!
	    window.open("http://0.0.0.0:4000/" +urlo);
	});
});
