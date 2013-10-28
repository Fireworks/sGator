$(document).ready(function(){
	$(document).on('click', '.course-add', function(){
		var cid = jQuery(this).attr('course-id');

		var json = JSON.stringify(cid);
		var csrftoken = $.cookie('csrftoken');
		
		$.ajax({
			headers: {"X-CSRFToken": csrftoken},
			url: '/schedule/',
			type: 'POST',
			data: cid,
			traditional: true,
			dataType: 'html',
			success: function(result){
				$.toast('Course added! View added courses on Create Schedule page.', {type: 'success'});
			}
		});
	});
});