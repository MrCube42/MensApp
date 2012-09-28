<?php

// used to collect food
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

// get the selected mensa or tarforst (1) by default
$selectedMensa = 1;
if (!empty($_GET)) {
	$selectedMensa = htmlspecialchars($_GET['mensa']);
}

// save weekdays with date and foodstring
$weekdays = array(0 => array('day' => null, 'food' => null), 1 => array('day' => null, 'food' => null), 2 => array('day' => null, 'food' => null), 3 => array('day' => null, 'food' => null), 4 => array('day' => null, 'food' => null));
// compute currently weekdays
$weekdays = weekNow($weekdays);

$openHours = "";

// check whether data is cached in file
$data = checkCache($weekdays, $selectedMensa);
// TODO: REMOVE FOR PRODUCTION
$data = null;
if ($data != null) {
	echo $data;
} else {
	$openHours = extractOpenHours(0, $weekdays, $selectedMensa);
	// if not, get stammessen for all weekdays
	for ($day = 0; $day < 5; $day++) {
		$weekdays = extractFood($day, $weekdays, $selectedMensa);
	}
	// and cave the result
	$data = saveJsonResult($openHours, $weekdays, $selectedMensa);
	echo $data;
}

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

// requests Studiwerk and extracts the XML-Code properly
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
					//TODO NEW: add students price
					$f = $subvalue['text'];
					if (sizeof($f) > 0) {
						$p = -1;
						if (array_key_exists("preis-1", $subvalue)) {
							$p = $subvalue['preis-1'];
							if (sizeof($p) <= 0) {
								$p = -1;
							}
						}
						if ($p == -1) {
							// tarforst, geomensa, schneidershof
							if (!$wasStammessen && (hasStammessenString($f) || isGeoMensaMenue1($menue, $selectedMensa) || $selectedMensa == 7)) {
								// if stammessen add stammessen price automatically
								$food -> foodMenu .= "<div class='price'>2,30</div><div class='reference'/>";
							} else {
								$food -> foodMenu .= "<div class='price noprice'>" . $p . "</div><div class='reference noprice'/>";
							}
						} else {
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

// removes (1,2,3,4,5) from the foodsstring
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
	// save to file
	$filename = $selectedMensa . '_mensafood_' . $date . '.xml';
	file_put_contents($filename, $json);
	// return json
	return $json;
}

// check whether result has been cached
function checkCache($weekdays, $selectedMensa) {
	$date = $weekdays[0]['day'] . '-' . $weekdays[4]['day'];
	$filename = $selectedMensa . '_mensafood_' . $date . '.xml';
	if (file_exists($filename)) {
		$data = file_get_contents($filename);
		return $data;
	} else {
		return null;
	}
}
?>