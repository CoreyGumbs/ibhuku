// Character Counter for profile bio text area box
$(document).ready(function(){

	//Profile Bio input limit. 
	var maxLength = 140;

	$('textarea').keyup(function(){
		var textLength =  $(this).val().length;
		var length = maxLength-textLength;
		$('#bio_character_feedback').text(length);
	});

	///Profile submission success/warning messages
	$('.messages').slideDown('slow').show();

	setTimeout(function(){
		$('.messages').slideUp('slow');
	},3000)
	
});