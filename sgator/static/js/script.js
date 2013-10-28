var courses = [];

$(document).ready(function(){
	$(document).on('click', '.course-add', function(){
		$.toast('Course added! View added courses on Create Schedule page.', {type: 'success'});
		var cid = jQuery(this).attr('course-id');
		courses.push(cid);
	});
});