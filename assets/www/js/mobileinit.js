// needed for phonegap
$(document).bind("mobileinit", function() {
	// Make your jQuery Mobile framework configuration changes here!
	$.support.cors = true;
	$.mobile.allowCrossDomainPages = true;
	$.mobile.defaultPageTransition = "fade";
	$.mobile.defaultDialogTransition = "fade";
	$.event.special.swipe.horizontalDistanceThreshold = 75;
});