// Character Counter for profile bio text area box

$(document).ready(function(){

	var maxLength = 150;

	$('textarea').keyup(function(){
		var length =  $(this).val().length;
		var length = maxLength-length;
		$('#bio_character_feedback').text(length);
	});
});