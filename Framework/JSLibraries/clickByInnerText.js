	var aTags = document.getElementsByTagName(arguments[0]);
	var found = 0;
	for (var i = 0; i < aTags.length; i++) {
  		if (aTags[i].textContent == arguments[1]) {
    			aTags[i].click();
    			found = 1;
    			break;
  		}
	}
	return found