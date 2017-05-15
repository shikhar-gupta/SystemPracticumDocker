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
	<h2>Student Information</h2>
	<?php 
		$sID = $_GET['sID'];

		//Setup our query
		$query = "SELECT * FROM Student where sID = '$sID'";
		 
		//Run the Query
		$result = mysqli_query($connection,$query);
		 
		//If the query returned results, loop through
		// each result
		if($result)
		{
		  while($row = mysqli_fetch_array($result))
		  {
		    echo "Name: " . $row["sID"] . " Student Name: ". $row['sName']. " GPA: " . $row['GPA'];
		  }
		}
		echo "<br>";
		$query = "SELECT * FROM Apply where sID = '$sID'";
		 
		//Run the Query
		$result = mysqli_query($connection,$query);
		 
		//If the query returned results, loop through
		// each result
		if($result)
		{
		  while($row = mysqli_fetch_array($result))
		  {
		    echo "Name: " . $row["sID"] . " College Name: ". $row['cName']. " Decision: " . $row['decision'];
		  }
		}

		echo "<br><br>Final Query<br>";

	
		$query = "select count(s.sID) from Student s inner join Apply a on a.sId = s.sID inner join College c on c.cName = a.cName where s.GPA > 8.8 AND a.decision = 'reject' AND c.enrollment > 1000;";
		 
		//Run the Query
		$result = mysqli_query($connection,$query);
		 
		//If the query returned results, loop through
		// each result
		if($result)
		{
		  while($row = mysqli_fetch_array($result))
		  {
		    echo "Count: ". $row["count(s.sID)"];
		  }
		}
	?>
</html>
