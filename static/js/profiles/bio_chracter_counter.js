// Character Counter for profile bio text area box

$(document).ready(function(){

	var maxLength = 140;

	$('textarea').keyup(function(){
		var textLength =  $(this).val().length;
		var length = maxLength-textLength;
		$('#bio_character_feedback').text(length);
	});
});