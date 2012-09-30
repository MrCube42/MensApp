<?php

/***
 *
 * Author: David Wuerfel (david@devinmotion.de)
 *
 * This script is used to extract food data from the Studentenwerk Trier for the MensApp version 2.0
 * I know that the code is rather ugly, but I think this results from PHP and some of its language
 * inherited problems and missing functionalities. I'm about to get rid of this script and replace it
 * with a more readable and elegant PYTHON script.
 *
 * The script works as follow: The first user that asks for food for a specific mensa numbered with
 * selectedMensa starts the script to fetch data from the Studentenwerk. After the data for this mensa
 * and time period is fetched, the fooddata will be simply saved to disk. Every following user that asks
 * for the same data will get the saved data from the file. I know that this could cause some problems
 * and I should replace this with a simple database and queries but this is a plan todo with the new
 * pyhton script.
 *
 * For the time being everything works ok
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

// save weekdays with date and foodstring
$weekdays = array(0 => array('day' => null, 'food' => null), 1 => array('day' => null, 'food' => null), 2 => array('day' => null, 'food' => null), 3 => array('day' => null, 'food' => null), 4 => array('day' => null, 'food' => null));
// compute current weekdays
$weekdays = weekNow($weekdays);

// check whether data is already cached in file
$data = checkCache($weekdays, $selectedMensa);
//// TODO: REMOVE FOR PRODUCTION
//$data = null;
// if not extract openHours, fooddata and save result to file
if ($data == null) {
	$openHours = extractOpenHours(0, $weekdays, $selectedMensa);
	// get stammessen for all weekdays
	for ($day = 0; $day < 5; $day++) {
		$weekdays = extractFood($day, $weekdays, $selectedMensa);
	}
	// and save the result
	$data = saveJsonResult($openHours, $weekdays, $selectedMensa);
}
echo $data;



 /**
  * Classes and Helpers
  * 
  **/
  
// helper class used to collect food
class Food {
	public $foodHead = "";
	public $foodMenu = "";
	public $foodPrice = "";
	public $stammEssenAdded = FALSE;
	public $alternativeAdded = FALSE;

	public function getFoodHeader() {
		if (strlen($this -> foodHead) > 0)
			return "<div class='theke'>" . $this -> foodHead . "</div>";
	}

	public function getFoodMenu() {
		if (strlen($this -> foodMenu) > 0)
			return "<div class='menu'>" . $this -> foodMenu . "</div>";
	}

	public function addStammEssenTag($string) {
		if (!$this -> stammEssenAdded) {
			if ($string != null && strpos($string, "<b>Vegetarisches STAMMESSEN</b>") > -1) {
				$this -> foodHead .= " - Vegetarisches Stammessen";
			} else {
				$this -> foodHead .= " - Stammessen";
			}
		}
		$this -> stammEssenAdded = TRUE;
	}

	public function addGeoStammEssenTag() {
		if (!$this -> stammEssenAdded) {
			$this -> foodHead .= "Stammessen";
		}
		$this -> stammEssenAdded = TRUE;
	}

	public function addAlternativeTag() {
		if (!$this -> alternativeAdded)
			$this -> foodHead .= " - Das alternative Menü";
		$this -> alternativeAdded = TRUE;
	}

}



/*
 * Functions and Helpers
 * 
 */
 
// compute weekdays that must be requested
function weekNow($weekdays) {
	// current weekday
	$weekday = date('w');
	$saturday = false;
	$sunday = false;
	// saturday -> go back to friday
	if ($weekday == 6) {
		$saturday = true;
		$weekday = 5;
	}
	// sunday -> go to monday
	if ($weekday == 0) {
		$sunday = true;
		$weekday = 1;
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
		$day = $today -> sub(new DateInterval('P' . ($weekday - 1) . 'D')) -> add(new DateInterval('P' . $i . 'D'));
		$weekdays[$i]['day'] = $day -> format('Ymd');
	}
	return $weekdays;
}

// extract the div that is used to present the opening hours of each mensa
function extractOpenHours($day, $weekdays, $selectedMensa) {
	$openHours = "";
	$targetUrl = "http://studiwerk.cms.rdts.de/cgi-bin/cms?_SID=NEW&_bereich=system&_aktion=export_speiseplan";
	$targetUrl = $targetUrl . '&datum=' . $weekdays[$day]['day'];
	$content = file_get_contents($targetUrl);

	// load xml and transform to array
	$xml = simplexml_load_string($content);
	$json = json_encode($xml);
	$array = json_decode($json, TRUE);

	$foods = "";
	$mensa = $array['mensa-' . $selectedMensa];

	if (array_key_exists('einstellungen', $mensa)) {
		if (array_key_exists("oeffnungszeit-1", $mensa['einstellungen'])) {
			$openHour = $mensa['einstellungen']['oeffnungszeit-1'];
			$openHours .= "<div class='openHoursNormal'>";
			if (strpos($openHour, ", ") > -1) {
				$openHour = explode(", ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else if (strpos($openHour, " | ") > -1) {
				$openHour = explode(" | ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else {
				$openHours .= "<div>" . $openHour . "</div>";
			}
			$openHours .= "</div>";
		}
		if (array_key_exists("oeffnungszeit-2", $mensa['einstellungen'])) {
			$openHour = $mensa['einstellungen']['oeffnungszeit-2'];
			$openHours .= "<div class='semesterferien'>Semesterferien:";
			if (strpos($openHour, ", ") > -1) {
				$openHour = explode(", ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else if (strpos($openHour, " | ") > -1) {
				$openHour = explode(" | ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else {
				$openHours .= "<div>" . $openHour . "</div>";
			}
			$openHours .= "</div>";
		}
		if (array_key_exists("oeffnungszeit", $mensa['einstellungen'])) {
			$openHour = $mensa['einstellungen']['oeffnungszeit'];
			$openHours .= "<div class='openHoursNormal'>";
			if (strpos($openHour, ", ") > -1) {
				$openHour = explode(", ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else if (strpos($openHour, " | ") > -1) {
				$openHour = explode(" | ", $openHour);
				foreach ($openHour as $key => $v) {
					$openHours .= "<div>" . $v . "</div>";
				}
			} else {
				$openHours .= "<div>" . $openHour . "</div>";
			}
			$openHours .= "</div>";
		}
	}
	if (strlen($openHours) <= 0) {
		$openHours .= "<div>keine Angaben</div>";
	}
	return $openHours;
}

// requests Studiwerk and extracts fooddata from the XML-Code
function extractFood($day, $weekdays, $selectedMensa) {
	$targetUrl = "http://studiwerk.cms.rdts.de/cgi-bin/cms?_SID=NEW&_bereich=system&_aktion=export_speiseplan";
	$targetUrl = $targetUrl . '&datum=' . $weekdays[$day]['day'];
	$content = file_get_contents($targetUrl);

	// load xml and transform to array
	$xml = simplexml_load_string($content);
	$json = json_encode($xml);
	$array = json_decode($json, TRUE);

	$foods = "";
	$mensa = $array['mensa-' . $selectedMensa];
	$menues = array();

	// look for general price
	$generalPrice = "";
	if (array_key_exists('einstellungen', $mensa)) {
		if (array_key_exists("preis", $mensa['einstellungen'])) {
			$generalPrice = $mensa['einstellungen']['preis'];
		} else if (array_key_exists("preis-1", $mensa['einstellungen'])) {
			$generalPrice = $mensa['einstellungen']['preis-1'];
		}
	}

	// go through all menues and all columns and collect food
	foreach ($mensa as $menue => $value) {
		// each menue
		if (strpos($menue, "menue") > -1) {
			$food = new Food();
			$wasStammessen = false;
			foreach ($value as $subkey => $subvalue) {
				// add title of theke or ausgabe
				if (strpos($subkey, "ausgabe") > -1) {
					$ausgabe = $value['ausgabe'];
					if (sizeof($ausgabe) > 0) {
						$food -> foodHead = $ausgabe;
					}
				}
				if (strpos($subkey, "titel") > -1) {
					$titel = $value['titel'];
					if (sizeof($titel) > 0) {
						$food -> foodHead = $titel;
					}
				}
				// look for stammessen or alternative string
				if (strpos($subkey, "zeile") > -1) {
					$f = $subvalue['text'];
					if (sizeof($f) > 0) {
						if (hasStammessenString($f)) {
							$food -> addStammEssenTag($f);
						}
						if (hasAlternativeString($f)) {
							$food -> addAlternativeTag();
						}
						if (isTarforstMenue1NotClosed($f, $menue, $selectedMensa)) {
							$food -> addStammEssenTag($f);
						}
						if (isGeoMensaMenue1($menue, $selectedMensa)) {
							$food -> addGeoStammEssenTag();
						}
					}
				}
				// collect each zeile (so the actual food)
				if (strpos($subkey, "zeile") > -1) {
					// get the meal itself
					$f = $subvalue['text'];
					if (sizeof($f) > 0) {
						// try to get the meals price
						$p = -1;
						if (array_key_exists("preis-1", $subvalue)) {
							$p = $subvalue['preis-1'];
							if (sizeof($p) <= 0) {
								$p = -1;
							}
						}
						if ($p == -1) {
							// if not directly connected to the food check for general food price
							if (!$wasStammessen && strlen($generalPrice) > 0) {
								$food -> foodMenu .= "<div class='price'>" . $generalPrice . "</div><div class='reference'/>";
							} else {
								$food -> foodMenu .= "<div class='price noprice'>" . $p . "</div><div class='reference noprice'/>";
							}
						} else {
							// add div to reference the price to the meal
							$food -> foodMenu .= "<div class='price'>" . $p . "</div><div class='reference'/>";
						}
						$wasStammessen = true;
						$food -> foodMenu .= "<div class='meal'>" . $f . "</div>";
					}
				}
			}
			// close menu
			array_push($menues, $food);
		}
	}

	// add each menu to the foods
	foreach ($menues as $key => $food) {
		$foods .= $food -> getFoodHeader();
		$foods .= $food -> getFoodMenu();
	}

	// align textoutput and remove unneccessary informatiom
	$foods = removeStammessenString($foods);
	$foods = removeAlternativeString($foods);
	$foods = removeNumberString($foods);
	$foods = removeWhitespaces($foods);
	
	// replace the icon markers with actual symbols
	$foods = putIcons($foods);

	// if no food info -> write info message
	if (strlen($foods) <= 0) {
		$foods = "<div class='menu'>keine Daten vorhanden</div>";
	}

	// add foods to current weekday
	$weekdays[$day]['food'] = $foods;
	return $weekdays;
}

// removes footnotes (1,2,3,4,5) from the foodsstring
function removeNumberString($string) {
	$string = preg_replace('/\([\d,]*\d\)/', '', $string);
	return $string;
}

// checks whether "Das alternative Menü" is in the foodsstring
function hasAlternativeString($string) {
	return strpos($string, "<b>Das alternative Menü</b>") > -1;
}

// removes "Das alternative Menü" from the foodsstring
function removeAlternativeString($string) {
	$string = preg_replace('/\<b>Das alternative Menü<\/b>/', '', $string);
	return $string;
}

// checks whether "STAMMESSEN" is in the foodsstring
function hasStammessenString($string) {
	$has = strpos($string, "<b>STAMMESSEN</b>") > -1;
	if (!$has) {
		$has = strpos($string, "<b>Vegetarisches STAMMESSEN</b>") > -1;
	}
	return $has;
}

// removes "STAMMESSEN" from the foodsstring
function removeStammessenString($string) {
	$string = preg_replace('/\<b>STAMMESSEN<\/b>,/', '', $string);
	$string = preg_replace('/\<b>Vegetarisches\sSTAMMESSEN<\/b>,/', '', $string);
	return $string;
}

// look whether tarforst has stammessen
function isTarforstMenue1NotClosed($string, $menue, $selectedMensa) {
	if ($selectedMensa == 1) {
		if (strpos($menue, "menue-1") > -1) {
			if (strpos($string, "geschlossen") > -1) {
				return FALSE;
			} else {
				return TRUE;
			}
		}
	}
	return FALSE;
}

// look whether if menue-1 from geomensa is selected -> so geo mensa stammessen
function isGeoMensaMenue1($menue, $selectedMensa) {
	if ($selectedMensa == 8) {
		if (strpos($menue, "menue-1") > -1) {
			return TRUE;
		}
	}
	return FALSE;
}

// removes unneccessary whitespace
function removeWhitespaces($string) {
	$string = preg_replace('/\s,/', ',', $string);
	$string = preg_replace('/\"\s/', '"', $string, 1);
	return $string;
}

// replaces icon marker with actual icons
function putIcons($string) {
	// setzte Symbole ein
	$string = preg_replace('/\[V\]/', "<img src='colored_icons/vegetarisch.gif' />", $string);
	$string = preg_replace('/\[R\]/', "<img src='colored_icons/rind.gif' />", $string);
	$string = preg_replace('/\[S\]/', "<img src='colored_icons/schwein.gif' />", $string);
	$string = preg_replace('/\[G\]/', "<img src='colored_icons/huhn.gif' />", $string);
	$string = preg_replace('/\[F\]/', "<img src='colored_icons/fisch.gif' />", $string);
	$string = preg_replace('/\[W\]/', "<img src='colored_icons/wild.gif' />", $string);
	$string = preg_replace('/\[M\]/', "<img src='colored_icons/laktosefrei.gif' />", $string);
	$string = preg_replace('/\[L\]/', "<img src='colored_icons/lamm.gif' />", $string);
	$string = preg_replace('/\[B\]/', "<img src='colored_icons/vegan.gif' />", $string);
	$string = preg_replace('/\[E\]/', "<img src='colored_icons/schlank.gif' />", $string);
	return $string;
}

// save the result to file for caching
function saveJsonResult($openHours, $weekdays, $selectedMensa) {
	// build json result
	$date = $weekdays[0]['day'] . '-' . $weekdays[4]['day'];
	$foodsArray = array();
	for ($i = 0; $i < 5; $i++) {
		//$foodsArray[$weekdays[$i]['day']] = $weekdays[$i]['food'];
		$foodsArray[$i] = $weekdays[$i]['food'];
	}
	$array = array("date" => $date, "mensaId" => $selectedMensa, "foods" => $foodsArray, "openHours" => $openHours);
	$json = json_encode($array);
	// save to file (ending 2.0 for new version)
	$filename = $selectedMensa . '_mensafood_' . $date . '_2.0.xml';
	file_put_contents($filename, $json);
	// return json
	return $json;
}

// check whether result has been cached
function checkCache($weekdays, $selectedMensa) {
	$date = $weekdays[0]['day'] . '-' . $weekdays[4]['day'];
	// ending 2.0 for new version
	$filename = $selectedMensa . '_mensafood_' . $date . '_2.0.xml';
	if (file_exists($filename)) {
		$data = file_get_contents($filename);
		return $data;
	} else {
		return null;
	}
}

?>