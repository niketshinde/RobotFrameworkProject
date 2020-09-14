 if (!window.jQuery) {
	var jquery = document.createElement('script'); jquery.type = 'text/javascript';
	jquery.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js';
	document.getElementsByTagName('head')[0].appendChild(jquery);
	}

$.getScript('https://the-internet.herokuapp.com/js/vendor/jquery.growl.js');

$('head').append('<link rel="stylesheet" href="https://the-internet.herokuapp.com/css/jquery.growl.css" type="text/css" />');

function loadjscssfile(filename, filetype){
	if (filetype=="js"){ //if filename is a external JavaScript file
		var fileref=document.createElement('script')
		fileref.setAttribute("type","text/javascript")
		fileref.setAttribute("src", filename)
	}
	else if (filetype=="css"){ //if filename is an external CSS file
		var fileref=document.createElement("link")
		fileref.setAttribute("rel", "stylesheet")
		fileref.setAttribute("type", "text/css")
		fileref.setAttribute("href", filename)
	}
	if (typeof fileref!="undefined")
		document.getElementsByTagName("head")[0].appendChild(fileref)
}

