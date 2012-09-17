// // before page is created - initial jQuery Mobile function
// $("#mainPage").live("pagebeforecreate", function(event) {
//
// // TODO USE FOR PRODUCTION !!!
// // phongap API uses
// function onDeviceReady() {
// // add menubutton function
// document.addEventListener("menubutton", openOptions, false);
// showAppetizerNotification = function(itemsFound) {
// navigator.notification.vibrate(250);
// var message = "";
// for(item in itemsFound) {
// message += item + " (";
// for(day in itemsFound[item]) {
// message += itemsFound[item][day];
// message += ",";
// }
// message = message.substr(0, message.lastIndexOf(','));
// message += "), ";
// }
// message = message.substr(0, message.lastIndexOf(', '));
// window.plugins.statusBarNotification.notify("MensAppetizer", message);
// }
// updateFoodData();
// }
//
// // phones back button can open options dialog
// function openOptions() {
// $.mobile.changePage("#options", {
// transition : "slidedown",
// role : "dialog"
// });
// }
//
// function selectMensa(event, ui) {
// selectedMensa = $("#mensaSelect option:selected")[0].value;
// saveSettings();
// updateFoodData();
// }
//
$(document).ready(function() {

	/** Initilization:
	 * 		- defining global variables
	 * 		- initialize event handlers
	 * 		- (re)load initial data and settings
	 */

	// global variables
	// Tarforst as default
	var selectedMensa = 1;
	var weekString = null;
	// holds the food data and the appetizer
	var data = {
		1 : null,
		2 : null,
		3 : null,
		4 : null,
		5 : null,
		6 : null,
		7 : null,
		8 : null,
		9 : null,
		10 : null,
		11 : null,
		12 : null
	};
	var useAppetizer = false;
	var appetizer = null;

	// event handlers
	$("#expandAll").bind("click", expandAll);
	$("#collapseAll").bind("click", collapseAll);

	// $("#mensaSelect").bind("change", selectMensa);
	// $('#appetizerInput').bind("change", addAppetizerInput);
	// $(".watchlistDelete").bind("click", deleteWatchlistItem);
	// $("#askDeleteData").bind("click", function() {
	// $("#sureData").show();
	// });
	// $("#askDeleteSettings").bind("click", function() {
	// $("#sureSettings").show();
	// });
	// $("#askDeleteAppetizer").bind("click", function() {
	// $("#sureAppetizer").show();
	// });
	// $(".notSure").bind("click", function() {
	// $(".sure").hide();
	// });
	$("#deleteData").bind("click", deleteDataCache);
	$("#deleteSettings").bind("click", deleteSettingsCache);

	// $("#deleteAppetizer").bind("click", deleteAppetizerCache);
	// $(".saveBackButton").bind("click", saveSettings);
	// $(".saveAppetizer").bind("click", saveAppetizer);

	// load initial data and settings
	loadTodaysDate();
	// loadSettings();

	expandActualWeekDay();

	// Now safe to use the PhoneGap API
	// document.addEventListener("deviceready", onDeviceReady, false);

	// // on page init (use this in jquery-mobile rather than document.ready)
	// $("#mainPage").live("pageinit", function(event) {
	// loadFoodData();
	// });
	// // load content into appetizer, when appetizer page is opened
	// $("#watchlist").live("pageinit", function(event) {
	// loadAppetizerContents();
	// });

	/**	Functions and Event Handlers
	 */

	// handles click on expand-button
	function expandAll() {
		$("#content").children().each(function(index, node) {
			$(this).trigger("expand");
		});
	}

	// handles click on collapse-button
	function collapseAll() {
		$("#content").children().each(function(index, node) {
			$(this).trigger("collapse");
		});
	}

	// loads the date of today and sets the date string presented under the mensapp title bar
	function loadTodaysDate() {
		var aDay = 86400000;
		var today = new Date();
		var weekday = new Date().getDay();
		// saturday -> go back to friday
		if (weekday == 6) {
			today = today - aDay;
			weekday = 5;
		}
		// sunday -> go to monday
		if (weekday == 0) {
			today = today.getTime() + aDay;
			weekday = 1;
		}
		var first = today - (weekday - 1) * aDay;
		var last = first + 4 * aDay;
		var date = new Date();
		date.setTime(first);
		var dateString = date.format("( dd.mm - ");
		date.setTime(last);
		dateString += date.format("dd.mm.yyyy )");
		$("#dateString").text(dateString);
	}

	// expands the current week day
	function expandActualWeekDay() {
		// expand day of the week
		var weekday = new Date().getDay();
		var isToday = true;
		// if saturday -> expand friday
		if (weekday == 6) {
			weekday = 5;
			isToday = false;
		}
		// if sunday -> expand monday
		if (weekday == 0) {
			weekday = 1;
			isToday = false;
		}
		// expand
		var actualDay = $("#content #day" + weekday);
		actualDay.trigger("expand");
		// style today
		if (isToday) {
			actualDay.addClass('today');
		}
	}

	function deleteDataCache() {
		console.log("DELETE DATA CACHE");
		// for ( i = 1; i <= 12; i++) {
		// localStorage.removeItem("mensapp:data:" + i);
		// }
		// data = {
		// 1 : null,
		// 2 : null,
		// 3 : null,
		// 4 : null,
		// 5 : null,
		// 6 : null,
		// 7 : null,
		// 8 : null,
		// 9 : null,
		// 10 : null,
		// 11 : null,
		// 12 : null
		// };
		// $(".sure").hide();
		window.setTimeout(function() {
			showMessage("Daten gelöscht.<br/>Werden wiederhergestellt.");
		}, 750)
		// showLoading();
		// updateFoodData();
	}

	function deleteSettingsCache() {
		console.log("DELETE SETTINGS");
		// localStorage.removeItem("mensapp:settings");
		// $(".sure").hide();
		// clearSettings();
	}

	// shows a message box that fades out
	function showMessage(message, messageHeader) {
		console.log("OPEN POPUP");
		$("#popupInfo h3").text(messageHeader);
		$("#popupInfo p").html(message);
		$("#popupInfo").popup("open");

		window.setTimeout(function() {
			$("#popupInfo").popup("close")
			// hide all other message boxes too
			// window.setTimeout(function() {
			// $(".messageBox").hide();
			// }, 1000)
		}, 1000);

	}

});

//
// // shows a message box that fades out
// function showMessage(message, messageHeader) {
// $(".messageBox h3").text(messageHeader);
// $(".messageBox p").html(message);
// $(".messageBox").show();
// window.setTimeout(function() {
// $(".messageBox").fadeOut(1000);
// // hide all other message boxes too
// window.setTimeout(function() {
// $(".messageBox").hide();
// }, 1000)
// }, 750);
// }
//

//
// // loads the current date and writes it to datestring
// function loadActualDate() {
// var aDay = 86400000;
// var today = new Date();
// var weekday = new Date().getDay();
// // saturday -> go back to friday
// if(weekday == 6) {
// today = today - aDay;
// weekday = 5;
// }
// // sunday -> go to monday
// if(weekday == 0) {
// today = today.getTime() + aDay;
// weekday = 1;
// }
// var first = today - (weekday - 1) * aDay;
// var last = first + 4 * aDay;
// var date = new Date();
// date.setTime(first);
// var dateString = date.format("( dd.mm - ");
// date.setTime(last);
// dateString += date.format("dd.mm.yyyy )");
// $("#dateString").text(dateString);
// }
//
// // show spinner while loading
// function showLoading() {
// // hide content and load
// $("#content").css("visibility", "hidden");
// $("#spinner").spin();
// $("#spinner").show();
// }
//
// // hide spinner after loading
// function hideLoading(hideContent) {
// // stop loading and show content
// $("#spinner").spin(false);
// $("#spinner").hide();
// if(!hideContent) {
// $("#content").css("visibility", "visible");
// }
// }
//
// function getSelectedMensaMapping(mensaId) {
// switch(mensaId) {
// case "1":
// return 0;
// case "8":
// return 1;
// case "2":
// return 2;
// // case "4":
// // return 3;
// // case "3":
// // return 6;
// // case "12":
// // return 11;
// case "7":
// return 3;
// case "5":
// return 4;
// // case "9":
// // return 8;
// // case "11":
// // return 10;
// case "10":
// return 5;
// case "6":
// return 6;
// default:
// return 0;
// }
// }
//
// function addAppetizerInput(event, ui) {
// addWatchlistItem(event.target.value);
// }
//
// function addWatchlistItem(item) {
// $("#watchlist ul").append("<li><a href='#'><h1 class='watchlistItem'>" + item + "</h1></a><a href='#' data-icon='delete' data-theme='e' class='watchlistDelete'></a></li>");
// $(".watchlistDelete").bind("click", deleteWatchlistItem);
// $("#watchlist ul").listview("refresh");
// $("#appetizerInput").val("");
// }
//
// function loadAppetizer() {
// // variable not set
// if(appetizer == null) {
// // get from local storage
// var storageAppetizer = localStorage.getItem("mensapp:appetizer");
// if(storageAppetizer != null) {
// appetizer = JSON.parse(storageAppetizer);
// }
// }
// }
//
// function loadAppetizerContents() {
// loadAppetizer();
// for(item in appetizer) {
// addWatchlistItem(appetizer[item]);
// }
// }
//
// function saveAppetizer() {
// oldAppetizer = appetizer;
// var toSave = new Array();
// $(".watchlistItem").each(function(index, node) {
// toSave.push($(this).text());
// });
// // set appetizer variable
// appetizer = toSave;
// // save appetizer in local storage
// toSave = JSON.stringify(toSave);
// localStorage.setItem("mensapp:appetizer", toSave);
// // look for appetizerfood if appetizer has changed
// if(!appetizersAreEqual(oldAppetizer, appetizer)) {
// lookForAppetizer();
// }
// }
//
// function appetizersAreEqual(oldAppetizer, newAppetizer) {
// var biggerAppetizer = oldAppetizer;
// // use biggest index
// if(oldAppetizer != null && newAppetizer.length > oldAppetizer.length) {
// biggerAppetizer = newAppetizer;
// }
// // compare each element
// for(index in biggerAppetizer) {
// if(oldAppetizer[index] != newAppetizer[index]) {
// return false;
// }
// }
// return true;
// }
//
// function removeAppetized() {
// if(data[selectedMensa] && data[selectedMensa].foods) {
// // remove appetized food
// $(".appetized").replaceWith(function() {
// return $(this).contents();
// });
// // reset food data
// for(var food in data[selectedMensa].foods) {
// data[selectedMensa].foods[food] = $('#se' + food).html();
// }
// }
// }
//
// function lookForAppetizer() {
// // first remove appetized data
// removeAppetized();
// if(!useAppetizer)
// return;
// // check only current selected mensa
// var itemsFound = {};
// var someFound = false;
// loadAppetizer();
// // add appetized food for the week if data is available
// if(data[selectedMensa] && data[selectedMensa].foods) {
// for(var food in data[selectedMensa].foods) {
// // look for all items from the appetizer
// for(var item in appetizer) {
// var regex = new RegExp(appetizer[item], "gi");
// var replacement = "<span class='appetized'>" + appetizer[item] + "</span>";
// // brace found item with css class appetized
// newFoodData = data[selectedMensa].foods[food].replace(regex, replacement);
// // if something has changed notify
// if(data[selectedMensa].foods[food] != newFoodData) {
// data[selectedMensa].foods[food] = newFoodData;
// var dayName = $("#se" + food).attr('data-day');
// if(itemsFound[appetizer[item]] == null) {
// itemsFound[appetizer[item]] = new Array();
// }
// itemsFound[appetizer[item]].push(dayName);
// someFound = true;
// }
// }
// }
// saveData();
// updateFoodDisplay();
// if(someFound) {
// showAppetizerNotification(itemsFound);
// }
// }
// }
//
// function showAppetizerNotification(itemsFound) {
// // a stub that is filled out after PhoneGap's deviceready Event is fired
// }
//
// function deleteWatchlistItem() {
// $(this).parent().remove();
// $("#watchlist ul").listview("refresh");
// }
//
// function updateFoodData() {
// $(".se").empty();
// $("#openHoursContent").empty();
// loadFoodData();
// }
//
// function updateFoodDisplay() {
// $(".se").empty();
// for(var food in data[selectedMensa].foods) {
// $("#se" + food).append(data[selectedMensa].foods[food]);
// }
// }
//
// function loadFoodData() {
// // check whether current data is cached
// restoreData();
// if(!data[selectedMensa]) {
// showLoading();
//
// // TODO CHANGE FOR PRODUCTION !!!
// // var targetUrl = "http://localhost/getfood.php";
// var targetUrl = "http://devinmotion.de/mensapp/getfood.php";
//
// var params = {
// "mensa" : selectedMensa
// };
//
// $.ajax({
// dataType : "json",
// async : true,
// url : targetUrl,
// data : params,
// success : function(jsonData, textStatus, jqXHR) {
// // cache data in local storage (HTML5)
// data[selectedMensa] = jsonData;
// saveData();
// processData();
// },
// error : function(jqXHR, textStatus, errorThrown) {
// showMessage("Aktueller Mensaplan kann nicht geladen werden.", "Fehler");
// hideLoading(true);
// }
// });
// } else {
// processData();
// }
// }
//
// function processData() {
// hideLoading();
// for(var food in data[selectedMensa].foods) {
// $("#se" + food).append(data[selectedMensa].foods[food]);
// }
// $("#openHoursContent").append(data[selectedMensa].openHours);
// lookForAppetizer();
// }
//
// function getDateKey() {
// if(weekString == null) {
// var aDay = 86400000;
// var today = new Date();
// var weekday = new Date().getDay();
// // saturday -> go back to friday
// if(weekday == 6) {
// today = today - aDay;
// weekday = 5;
// }
// // sunday -> go to monday
// if(weekday == 0) {
// today = today.getTime() + aDay;
// weekday = 1;
// }
// var first = today - (weekday - 1) * aDay;
// var last = first + 4 * aDay;
// var date = new Date();
// date.setTime(first);
// weekString = date.format("yyyymmdd");
// date.setTime(last);
// weekString += "-" + date.format("yyyymmdd");
// }
// return weekString;
// }
//
// function deleteDataCache() {
// for( i = 1; i <= 12; i++) {
// localStorage.removeItem("mensapp:data:" + i);
// }
// data = {
// 1 : null,
// 2 : null,
// 3 : null,
// 4 : null,
// 5 : null,
// 6 : null,
// 7 : null,
// 8 : null,
// 9 : null,
// 10 : null,
// 11 : null,
// 12 : null
// };
// $(".sure").hide();
// showMessage("Daten gelöscht.<br/>Werden wiederhergestellt.")
// showLoading();
// updateFoodData();
// }
//

//
// function clearSettings() {
// $("#selectedMensaOption")[0].checked = false;
// $("#selectedMensaOption").trigger("click");
// $("#selectedMensaOption")[0].checked = false;
// $("#useAppetizerOption")[0].checked = false;
// $("#useAppetizerOption").trigger("click");
// $("#useAppetizerOption")[0].checked = false;
// useAppetizer = false;
// }
//
// function deleteAppetizerCache() {
// localStorage.removeItem("mensapp:appetizer");
// appetizer = null;
// $("#watchlist ul").contents().remove();
// $("#watchlist ul").listview("refresh");
// $(".sure").hide();
// }
//
// function loadSettings() {
// var settings = localStorage.getItem("mensapp:settings");
// if(settings == null)
// return null;
// settings = JSON.parse(settings);
// if(settings["selectedMensaOption"] == true) {
// selectedMensa = settings["selectedMensa"];
// $("#selectedMensaOption")[0].checked = true;
// $("#mensaSelect")[0].options[getSelectedMensaMapping(settings["selectedMensa"])].selected = true;
// } else {
// $("#selectedMensaOption")[0].checked = false;
// $("#selectedMensaOption").trigger("click");
// $("#selectedMensaOption")[0].checked = false;
// }
// if(settings["useAppetizerOption"] == true) {
// $("#useAppetizerOption")[0].checked = true;
// useAppetizer = true;
// } else {
// $("#useAppetizerOption")[0].checked = false;
// $("#useAppetizerOption").trigger("click");
// $("#useAppetizerOption")[0].checked = false;
// }
// }
//
// function saveSettings() {
// var hasUsedAppetizer = useAppetizer;
// var selectedMensaChecked = $("#selectedMensaOption")[0].checked;
// var useAppetizerChecked = $("#useAppetizerOption")[0].checked;
// var toSave = {
// "selectedMensaOption" : selectedMensaChecked,
// "selectedMensa" : selectedMensa,
// "useAppetizerOption" : useAppetizerChecked
// };
// toSave = JSON.stringify(toSave);
// localStorage.setItem("mensapp:settings", toSave);
// if(useAppetizerChecked) {
// useAppetizer = true;
// // if appetizer is checked now
// if(!hasUsedAppetizer) {
// lookForAppetizer();
// }
// } else {
// useAppetizer = false;
// // is not appetized -> just remove appetized food
// removeAppetized();
// }
// }
//
// function saveData() {
// toSave = JSON.stringify(data[selectedMensa]);
// localStorage.setItem("mensapp:data:" + selectedMensa, toSave);
// }
//
// function restoreData() {
// // get data from variable or localStorage
// if(!data[selectedMensa]) {
// // first check localStorage
// var mensaData = localStorage.getItem("mensapp:data:" + selectedMensa);
// if(!mensaData)
// return;
// data[selectedMensa] = JSON.parse(mensaData);
// }
// // data is available but time is not set correct
// if(getDateKey() != data[selectedMensa]["date"]) {
// localStorage.removeItem("mensapp:data:" + selectedMensa);
// // reset
// data[selectedMensa] = null;
// return;
// }
// // otherwise its the right date
// else {
// return data[selectedMensa];
// }
// }
//
// function showOpenHours() {
// $("#overall").css("transform", "translate(0, 0)");
// $("#overall").css("-webkit-transform", "translate(0, 0)");
// $("#overall").css("-moz-transform", "translate(0, 0)");
// $("#overall").css("-ms-transform", "translate(0, 0)");
// $("#overall").css("-o-transform", "translate(0, 0)");
// $("#expandAll").hide();
// $("#collapseAll").hide();
// $(".iconhelp").hide();
// window.setTimeout(function() {
// $("#content").hide();
// }, 500);
// }
//
// function showContent() {
// $("#content").show();
// $("#expandAll").show();
// $("#collapseAll").show();
// $(".iconhelp").show();
// $("#overall").css("transform", "translate(-50%, 0)");
// $("#overall").css("-webkit-transform", "translate(-50%, 0)");
// $("#overall").css("-moz-transform", "translate(-50%, 0)");
// $("#overall").css("-ms-transform", "translate(-50%, 0)");
// $("#overall").css("-o-transform", "translate(-50%, 0)");
// }
//
// // global variables
// // Tarforst as default
// var selectedMensa = 1;
// var weekString = null;
// // holds the food data and the appetizer
// var data = {
// 1 : null,
// 2 : null,
// 3 : null,
// 4 : null,
// 5 : null,
// 6 : null,
// 7 : null,
// 8 : null,
// 9 : null,
// 10 : null,
// 11 : null,
// 12 : null
// };
// var useAppetizer = false;
// var appetizer = null;
//
// $("#mensaSelect").bind("change", selectMensa);
//

//
// $('#appetizerInput').bind("change", addAppetizerInput);
// $(".watchlistDelete").bind("click", deleteWatchlistItem);
//
// $("#askDeleteData").bind("click", function() {
// $("#sureData").show();
// });
// $("#askDeleteSettings").bind("click", function() {
// $("#sureSettings").show();
// });
// $("#askDeleteAppetizer").bind("click", function() {
// $("#sureAppetizer").show();
// });
// $(".notSure").bind("click", function() {
// $(".sure").hide();
// });

// $("#deleteAppetizer").bind("click", deleteAppetizerCache);
// $(".saveBackButton").bind("click", saveSettings);
// $(".saveAppetizer").bind("click", saveAppetizer);
//
// $("#overall").bind("swiperight", showOpenHours);
// $("#overall").bind("swipeleft", showContent);
//
// loadActualDate();
// loadSettings();
// expandActualWeekDay();
// // Now safe to use the PhoneGap API
// document.addEventListener("deviceready", onDeviceReady, false);
//
// // on page init (use this in jquery-mobile rather than document.ready)
// $("#mainPage").live("pageinit", function(event) {
// loadFoodData();
// });
// // load content into appetizer, when appetizer page is opened
// $("#watchlist").live("pageinit", function(event) {
// loadAppetizerContents();
// });
// });
