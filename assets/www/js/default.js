/***
 * Author: David Wuerfel (david@devinmotion.de)
 ***/

// before page is created - initial jQuery Mobile function
$("#mainPage").live("pagebeforecreate", function (event) {

    /** Phonegap Initilization:
     *         - defining menubutton handling
     *         - defining notification behavior when appetizers found
     */

        // TODO: COMMENT-IN AND USE FOR PRODUCTION !!!
        // phonegap API uses
    function onDeviceReady() {
        // add menubutton function -> open options
        document.addEventListener("menubutton", function () {
            // phones back button can open options page
            $.mobile.changePage("#options", {
                transition:"slideup",
                role:"page"
            });
        }, false);

        // add notification handling on found appetized food
        showAppetizerNotification = function (itemsFound) {
            navigator.notification.vibrate(250);
            var message = "";
            for (item in itemsFound) {
                message += item + " (";
                for (day in itemsFound[item]) {
                    message += itemsFound[item][day];
                    message += ",";
                }
                message = message.substr(0, message.lastIndexOf(','));
                message += "), ";
            }
            message = message.substr(0, message.lastIndexOf(', '));
            window.plugins.statusBarNotification.notify("MensAppetizer", message);
        }
    }


    /** Basic Initilization:
     *         - defining global variables
     *         - initialize event handlers
     *         - (re)load initial data and settings
     */

    // global variables
    // tarforst as default
    var selectedMensa = 1;
    var weekString = null;
    var foodData = {
        1:null,
        2:null,
        3:null,
        4:null,
        5:null,
        6:null,
        7:null,
        8:null,
        9:null,
        10:null,
        11:null,
        12:null
    };
    var useAppetizer = false;
    var appetizer = null;

    // time value constants
    var MESSAGE_APPEARANCE_TIME = 1000;
    var DELETING_TIME = 500;
    var TIME_TILL_POPOUT = 150;

    // event handlers
    $("#expandAll").bind("click", expandAll);
    $("#collapseAll").bind("click", collapseAll);

    $("#mensaSelect").bind("change", selectMensa);

    $("#appetizerInput").bind("keydown", addAppetizerInput);
    // live binds to this element and all future elements
    $(".watchlistItem").live("click", copyWatchlistItem);
    $(".watchlistDelete").live("click", deleteWatchlistItem);

    $("#deleteFoodData").bind("click", deleteFoodDataCache);
    $("#deleteSettings").bind("click", deleteSettingsCache);
    $("#deleteAppetizer").bind("click", deleteAppetizerCache);

    $(".saveBackButton").bind("click", saveSettings);
    $(".saveAppetizer").bind("click", saveAppetizer);

    // close open hours popup on click/touch
    $("#popupOpenHours").live("click", closeOpenHours);

    // load initial data and settings
    loadDateStrings();
    loadSettings();

    expandWeekDayToday();

    // TODO: COMMENT-IN AND USE FOR PRODUCTION!!!
    // Now safe to use the PhoneGap API
    document.addEventListener("deviceready", onDeviceReady, false);

    // jquery mobile initialization
    // on page init (use this in jquery-mobile rather than document.ready)
    $("#mainPage").live("pageshow", function (event) {
        loadFoodData();
    });
    // load content into appetizer, when appetizer page is opened
    $("#watchlist").live("pageinit", function (event) {
        loadAppetizerContents();
    });


    /**    Functions and Event Handlers
     */

        // handles click on expand-button
    function expandAll() {
        $("#content").children().each(function (index, node) {
            $(this).trigger("expand");
        });
    }

    // handles click on collapse-button
    function collapseAll() {
        $("#content").children().each(function (index, node) {
            $(this).trigger("collapse");
        });
    }

    // when the user selects a mensa from the mensaselector at the bottom
    function selectMensa() {
        selectedMensa = $("#mensaSelect option:selected")[0].value;
        saveSettings();
        updateFoodData();
    }

    // loads the date of today, sets the date string presented under the mensapp title bar
    // and the week string used to load food data for the correct week
    function loadDateStrings() {
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
        // compute string to represent the actual week in the frontend
        date.setTime(first);
        var dateString = date.format("( dd.mm - ");
        date.setTime(last);
        dateString += date.format("dd.mm.yyyy )");
        $("#dateString").text(dateString);

        // compute string representing the week for loading fooddata in the backend
        date.setTime(first);
        weekString = date.format("yyyymmdd");
        date.setTime(last);
        weekString += "-" + date.format("yyyymmdd");
    }

    // expands the current weekday
    function expandWeekDayToday() {
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
        var today = $("#content #day" + weekday);
        today.attr("data-collapsed", "false");
        // style today
        if (isToday) {
            today.addClass('today');
        }
    }

    // deletes all the fooddata cache in local storage
    function deleteFoodDataCache() {
        for (i = 1; i <= foodData.length; i++) {
            localStorage.removeItem("mensapp:data:" + i);
        }

        window.setTimeout(function () {
            showMessage("Daten gelöscht. Werden nun wiederhergestellt.", "", "options");
            // after
            window.setTimeout(function () {
                updateFoodData();
            }, MESSAGE_APPEARANCE_TIME)
        }, DELETING_TIME)
    }

    // clears the menu entries and updates the fooddata
    function updateFoodData() {
        $(".menuEntry").empty();
        foodData = {
            1:null,
            2:null,
            3:null,
            4:null,
            5:null,
            6:null,
            7:null,
            8:null,
            9:null,
            10:null,
            11:null,
            12:null
        };
        loadFoodData();
    }

    // loads the fooddata
    function loadFoodData() {
        // check whether current data is cached
        restoreData();
        if (!foodData[selectedMensa]) {
            showLoading();

            // use new script for new MensApp version 2.0
            // TODO: CHANGE FOR PRODUCTION !!!
//            var targetUrl = "http://localhost/getfood_2.0.php";
            var targetUrl = "http://devinmotion.de/mensapp/getfood_2.0.php";

            var params = {
                "mensa":selectedMensa
            };

            $.ajax({
                dataType:"json",
                async:true,
                url:targetUrl,
                data:params,
                success:function (jsonData, textStatus, jqXHR) {
                    // cache data in local storage (HTML5)
                    foodData[selectedMensa] = jsonData;
                    saveFoodData();
                    processFoodData();
                    processOpenHours();
                },
                error:function (jqXHR, textStatus, errorThrown) {
                    hideLoading(true);
                    showMessage("Aktueller Mensaplan kann nicht geladen werden.", "Fehler", "content");
                }
            });
        } else {
            processFoodData();
            processOpenHours();
        }

        // shows fooddata in frontend and looks for appetizer
        function processFoodData() {
            hideLoading();
            for (var food in foodData[selectedMensa].foods) {
                // clear first
                $("#me" + food).empty()
                $("#me" + food).append(foodData[selectedMensa].foods[food]);
            }
            lookForAppetizer();
        }

        // adds open hours to the open hours content
        function processOpenHours() {
            $("#openHoursHeader").empty();
            $("#openHoursHeader").append("Öffnungszeiten<br/>" + $("#mensaSelect option:selected")[0].text);
            $("#openHoursContent").empty();
            $("#openHoursContent").append(foodData[selectedMensa].openHours);
        }

        // restores the fooddata from the localstorage if available
        function restoreData() {
            // get data from variable or localStorage
            if (!foodData[selectedMensa]) {
                // first check localStorage
                var mensaData = localStorage.getItem("mensapp:data:" + selectedMensa);
                if (!mensaData)
                    return;
                foodData[selectedMensa] = JSON.parse(mensaData);
            }
            // data is available but time is not set correct
            if (weekString != foodData[selectedMensa]["date"]) {
                localStorage.removeItem("mensapp:data:" + selectedMensa);
                // reset
                foodData[selectedMensa] = null;
                return;
            }
            else {
                // otherwise its the right date
                return foodData[selectedMensa];
            }
        }
    }


    // saves fooddata of selected mensa to localstorage
    function saveFoodData() {
        toSave = JSON.stringify(foodData[selectedMensa]);
        localStorage.setItem("mensapp:data:" + selectedMensa, toSave);
    }

    // deletes all settings of mensapp from the localstorage and adjusts frontend controls
    function deleteSettingsCache() {
        localStorage.removeItem("mensapp:settings");
        // little workaround because triggering of options doesn't work properly
        $("#selectedMensaOption")[0].checked = false;
        $("#selectedMensaOption").trigger("click");
        $("#selectedMensaOption")[0].checked = false;
        $("#useAppetizerOption")[0].checked = false;
        $("#useAppetizerOption").trigger("click");
        $("#useAppetizerOption")[0].checked = false;
        useAppetizer = false;
    }

    // saves all the settings to the localstorage
    function saveSettings() {
        var hasUsedAppetizer = useAppetizer;
        var selectedMensaChecked = $("#selectedMensaOption")[0].checked;
        var useAppetizerChecked = $("#useAppetizerOption")[0].checked;
        var toSave = {
            "selectedMensaOption":selectedMensaChecked,
            "selectedMensa":selectedMensa,
            "useAppetizerOption":useAppetizerChecked
        };
        toSave = JSON.stringify(toSave);
        localStorage.setItem("mensapp:settings", toSave);
        if (useAppetizerChecked) {
            useAppetizer = true;
            // if appetizer is checked now
            if (!hasUsedAppetizer) {
                lookForAppetizer();
            }
        } else {
            useAppetizer = false;
            // is not appetized -> just remove appetized food
            removeAppetizedFood();
        }
    }

    // loads all the settings from the localstorage if available
    function loadSettings() {
        var settings = localStorage.getItem("mensapp:settings");
        if (settings == null)
            return null;
        settings = JSON.parse(settings);
        if (settings["selectedMensaOption"] == true) {
            selectedMensa = settings["selectedMensa"];
            $("#selectedMensaOption")[0].checked = true;
            $("#mensaSelect")[0].options[getSelectedMensaMapping(settings["selectedMensa"])].selected = true;
        } else {
            $("#selectedMensaOption")[0].checked = false;
            $("#selectedMensaOption").trigger("click");
            $("#selectedMensaOption")[0].checked = false;
        }
        if (settings["useAppetizerOption"] == true) {
            $("#useAppetizerOption")[0].checked = true;
            useAppetizer = true;
        } else {
            $("#useAppetizerOption")[0].checked = false;
            $("#useAppetizerOption").trigger("click");
            $("#useAppetizerOption")[0].checked = false;
        }

        // little helper that maps mensaId to selected mensa in the selection
        function getSelectedMensaMapping(mensaId) {
            switch (mensaId) {
                case "1":
                    return 0;
                case "8":
                    return 1;
                case "2":
                    return 2;
                // case "4":
                // return 3;
                // case "3":
                // return 6;
                // case "12":
                // return 11;
                case "7":
                    return 3;
                case "5":
                    return 4;
                // case "9":
                // return 8;
                // case "11":
                // return 10;
                case "10":
                    return 5;
                case "6":
                    return 6;
                default:
                    return 0;
            }
        }
    }

    // deletes appetizer settings from the localstorage and adjusts appetizer frontend
    function deleteAppetizerCache() {
        localStorage.removeItem("mensapp:appetizer");
        appetizer = null;
        $("#watchlist ul").contents().remove();
        $("#watchlist ul").listview("refresh");
    }

    // save appetizer to localstorage
    function saveAppetizer() {
        var oldAppetizer = appetizer;
        var toSave = new Array();
        $(".watchlistItem").each(function (index, node) {
            toSave.push($(this).text());
        });
        // set appetizer variable
        appetizer = toSave;
        // save appetizer in local storage
        toSave = JSON.stringify(toSave);
        localStorage.setItem("mensapp:appetizer", toSave);
        // look for appetizerfood if appetizer has changed
        if (!appetizersAreEqual(oldAppetizer, appetizer)) {
            lookForAppetizer();
        }

        // helper function that checks whether two appetizers are equal
        function appetizersAreEqual(oldAppetizer, newAppetizer) {
            var biggerAppetizer = oldAppetizer;
            // use biggest index
            if (oldAppetizer != null && newAppetizer.length > oldAppetizer.length) {
                biggerAppetizer = newAppetizer;
            }
            // compare each element
            for (index in biggerAppetizer) {
                if (oldAppetizer[index] != newAppetizer[index]) {
                    return false;
                }
            }
            return true;
        }
    }

    // if appetizer not in local variable try localstorage
    function loadAppetizer() {
        // variable not set
        if (appetizer == null) {
            // get from local storage
            var storageAppetizer = localStorage.getItem("mensapp:appetizer");
            if (storageAppetizer != null) {
                appetizer = JSON.parse(storageAppetizer);
            }
        }
    }

    // loads the appetizer watchlist items
    function loadAppetizerContents() {
        loadAppetizer();
        for (var item in appetizer) {
            addWatchlistItem(appetizer[item]);
        }
    }

    // a stub that is filled out after PhoneGap's deviceready Event is fired
    function showAppetizerNotification(itemsFound) {
        // stub to be filled after PhoneGap's deviceready Event is fired
    }

    // check food data for appetized food
    function lookForAppetizer() {
        // first remove appetized data
        removeAppetizedFood();
        if (!useAppetizer)
            return;
        // check only current selected mensa
        var itemsFound = {};
        var someFound = false;
        loadAppetizer();
        // add appetized food for the week if data is available
        if (foodData[selectedMensa] && foodData[selectedMensa].foods) {
            for (var food in foodData[selectedMensa].foods) {
                // look for all items from the appetizer
                for (var item in appetizer) {
                    var regex = new RegExp(appetizer[item], "gi");
                    var replacement = "<span class='appetized'>" + appetizer[item] + "</span>";
                    // brace found item with css class appetized
                    var newFoodData = foodData[selectedMensa].foods[food].replace(regex, replacement);
                    // if something has changed notify
                    if (foodData[selectedMensa].foods[food] != newFoodData) {
                        foodData[selectedMensa].foods[food] = newFoodData;
                        var dayName = $("#se" + food).attr('data-day');
                        if (itemsFound[appetizer[item]] == null) {
                            itemsFound[appetizer[item]] = new Array();
                        }
                        itemsFound[appetizer[item]].push(dayName);
                        someFound = true;
                    }
                }
            }
            saveFoodData();
            updateFoodDisplay();
            if (someFound) {
                showAppetizerNotification(itemsFound);
            }
        }

        // helper function that cleans menu entries and updates with appetized food
        function updateFoodDisplay() {
            $(".menuEntry").empty();
            for (var food in foodData[selectedMensa].foods) {
                $("#me" + food).append(foodData[selectedMensa].foods[food]);
            }
        }
    }

    // removes appetized classes from HTML that marked food entries as appetized
    function removeAppetizedFood() {
        if (foodData[selectedMensa] && foodData[selectedMensa].foods) {
            // remove appetized food
            $(".appetized").replaceWith(function () {
                return $(this).contents();
            });
        }
    }

    // add item to watch to the appetizer
    function addAppetizerInput(event, ui) {
        // is return pressed
        var input = event.target.value;
        if (event.keyCode == 13 && input != "") {
            addWatchlistItem(input);
        }
    }

    // add watchlist item to appetizer frontend
    function addWatchlistItem(item) {
        $("#watchlist ul").append("<li><a href='#' class='watchlistItem'>" + item + "</a><a href='#' data-icon='delete' data-theme='a' class='watchlistDelete'></a></li>");
        $("#appetizerInput").val("");
        $("#watchlist ul").listview("refresh");
    }

    // copies a watchlist item to the input field
    function copyWatchlistItem(event, ui) {
        $("#appetizerInput").val(event.target.innerText);
    }

    // removes a watchlist item from the appetizer frontend
    function deleteWatchlistItem() {
        $(this).parent().remove();
        $("#watchlist ul").listview("refresh");
    }

    // close openHours on click/touch
    function closeOpenHours() {
        // workaround for strange behavior on popout
        $("#popupOpenHours").hide();
        $("#popupOpenHours").popup("close");
        window.setTimeout(function () {
            $("#popupOpenHours").show();
        }, TIME_TILL_POPOUT);
    }

    // shows a message box that fades out
    function showMessage(message, messageHeader, origin) {
        var popupId = "#popupInfo-" + origin;
        $(popupId + " h3").text(messageHeader);
        $(popupId + " p").html(message);
        $(popupId).popup("open");

        // close popup after some time
        window.setTimeout(function () {
            $(popupId).popup("close");
        }, MESSAGE_APPEARANCE_TIME);
    }

    // show spinner, hide content and disable select menu while loading
    function showLoading() {
        // hide content and load
        $("#content").css("visibility", "hidden");
        // wait a moment and disable select menu
        window.setTimeout(function () {
            $("#mensaSelect").selectmenu("disable");
        }, TIME_TILL_POPOUT);
        $.mobile.loading("show");
    }

    // hide spinner, show content and enable select menu after loading
    function hideLoading(hideContent) {
        $.mobile.loading("hide");
        // wait a moment and enable select menu
        window.setTimeout(function () {
            $("#mensaSelect").selectmenu("enable");
        }, TIME_TILL_POPOUT);
        if (!hideContent) {
            $("#content").css("visibility", "visible");
        }
    }

});