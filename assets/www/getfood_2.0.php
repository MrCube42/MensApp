<?php

/***
 *
 * Author: David Wuerfel (david@devinmotion.de)
 *
 * This script is used to extract food data from the Studentenwerk Trier for the MensApp version 2.0
 * Since PHP code can be rather ugly and unstructured I built a new version for data extraction in python.
 * This python server is hosted in Google App Engine. However the MensApp still called the old getfood php.
 * Therefore we have to simply route this call to the new python script.
 * This should work for the time being until the new MensApp version can directly use the python server.
 *
 ***/

/**
 * Start of getfood script
 **/

// get the selected mensa or tarforst (1) by default
$selectedMensa = 1;
if (!empty($_GET)) {
	$selectedMensa = htmlspecialchars($_GET['mensa']);
	// check whether this is a proper mensa value
	if (!($selectedMensa != 1 || $selectedMensa != 2 || $selectedMensa != 5 || $selectedMensa != 6 || $selectedMensa != 7 || $selectedMensa != 8 || $selectedMensa != 10)) {
		$selectedMensa = 1;
	}
}

// the structure of the mensa ids change with a new version of the SWT xml data
// therefore we have to map the old values to the new one
// 1 -> 1, 2 -> 2,  8 <- 3, 2 <- 2, 7 <- 4, 5 <- 4, 10 <-6, 6 <- 5
switch($selectedMensa) {
	case 1: break; // Mensa Tarforst
	case 2: break; // Mensa Bistro
	case 5: $selectedMensa = 4; break; // Schneidershof (kleine Karte)
	case 6: $selectedMensa = 5; break; // Irminenfreihof
	case 7: $selectedMensa = 4; break; // Mensa Schneidershof
	case 8: $selectedMensa = 3; break; // Mensa Petrisberg
	case 10: $selectedMensa = 6; break; // Kindergarten
}

// get datespan string
$weekdays = GetCurrentWeekDays();
$datespan = $weekdays[0] . '-' . $weekdays[4];

// fet from new python script
$baseUrl = "http://devinmotion-mensapp-server.appspot.com/";
$arguments = "mensa=" . $selectedMensa . "&datespan=" . $datespan;
$targetUrl = $baseUrl . "?" . $arguments;
$jsonDataResponse = file_get_contents($targetUrl);

echo $jsonDataResponse;

/*
 * Helpers
 *
 */
// compute weekdays that must be requested
function GetCurrentWeekDays() {
	$weekdays = array(0 => null, 1 => null, 2 => null, 3 => null, 4 => null);
	// get current weekday
	$currentWeekday = date('w');
	$saturday = false;
	$sunday = false;
	// saturday -> go back to friday
	if ($currentWeekday == 6) {
		$saturday = true;
		$currentWeekday = 5;
	}
	// sunday -> go to monday
	if ($currentWeekday == 0) {
		$sunday = true;
		$currentWeekday = 1;
	}
	// compute weekdays
	for ($i = 0; $i < 5; $i++) {
		$today = new DateTime;
		if ($saturday) {
			$today = $today -> sub(new DateInterval('P1D'));
		}
		if ($sunday) {
			$today = $today -> add(new DateInterval('P1D'));
		}
		$day = $today -> sub(new DateInterval('P' . ($currentWeekday - 1) . 'D')) -> add(new DateInterval('P' . $i . 'D'));
		$weekdays[$i] = $day -> format('Ymd');
	}
	return $weekdays;
}

?>