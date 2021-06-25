console.log(data);
hobby_id = data['hobby_id'];
comment_id = data['comment_id'];
var r;
$.ajax({
	type : "POST",
	url : "user/praise_add/" + comment_id,
	data : {'relateItemNodeId' : hobby_id},
    async: false,
	success : function(result) {
		console.log(result);
		if (result.success) {
			r="1";
		} else {
			r="0";
		}
	}
});
r;