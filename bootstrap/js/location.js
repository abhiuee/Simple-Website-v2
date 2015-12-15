function clicked(cb) {
	//If save location is checked then use this
	var x = cb.checked;
	if (x ) {
		console.log(x)
		console.log("Checked")
		var b = document.getElementById("hidden_location");
    	b.value = "True";
	}
}