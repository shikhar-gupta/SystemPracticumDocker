 <?php
ini_set('display_errors', 1);
$servername = "mysql";
$username = "root";
$password = "sata";
$dbname = "CS309";

$connection = mysqli_connect($servername, $username, $password,$dbname);
?>

<html>
	<head>
		<title>Student Database</title>
	</head>
	<h1> Welcome to Student Database </h1>
	<h2>Student Retrival</h2>
	<form action = "/display.php" method = "get">
	<label>Enter student id: <label>
	<input type = "text" value = "Student ID" name = "sID">
	<button type = "submit">Search</button>
	</form>
</html>

<?php 
		echo "<br>";
		$query = "SHOW TABLES;";
		 
		//Run the Query
		$result = mysqli_query($connection,$query);
		 
		//If the query returned results, loop through
		// each result
		if($result)
		{
		  while($row = mysqli_fetch_array($result))
		  {
		    print_r($row);
		  }
		}
?>
