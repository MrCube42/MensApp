// needed for phonegap
$(document).bind("mobileinit", function() {
	// Make your jQuery Mobile framework configuration changes here!
	$.support.cors = true;
	$.mobile.allowCrossDomainPages = true;
	$.mobile.defaultPageTransition = "slideup";
	$.mobile.defaultDialogTransition = "pop";
    // defaults for loader
    $.mobile.loader.prototype.options.text = "...Lade Daten vom Studiwerk...";
    $.mobile.loader.prototype.options.textVisible = true;
    // collapsible as insets
    $.mobile.collapsible.prototype.options.inset = false;
});