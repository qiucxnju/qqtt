var TagManager = new Object();
TagManager.readTags = function(d) {
	var tags = [];
	$(d).each(function() {
		var tag = $(this).attr('value');
		tags.push(tag);
	})
	return tags;
}
TagManager.loadTags = function(tags, func) {
	$.ajax({
		url: "/ajax/loadTags",
		data: {
			tags: JSON.stringify(tags)
		}
	}).done(function(data) {
		func(data);
	});
}
TagManager.markdown = function(content, func) {
	$.ajax({
		type: "POST",
		url: "/ajax/markDown",
		data: {
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
			content: content
		}
	}).done(function(data) {
		func(data);
	});
}


function addTag(value) {
	var tags = TagManager.readTags('#selectedTag .tag');
	if ($.inArray(value, tags) < 0) {
		$('#selectedTag').append('<input type="button" class="tag btn btn-dark" onclick="deleteThis(this)" value="' + value + '"/>');
	}
	$('#tagDialogTrigger').click();
};

function loadTag() {
        console.log("aaaa");
	TagManager.loadTags(TagManager.readTags('#selectedTag .tag'), function(data) {
        console.log("aaaa");
		var tagList = JSON.parse(data);
		$("#tagList").empty();
        console.log("aaaa");
		for (x in tagList) {
			var tag = tagList[x];
			$("#tagList").append(' <li class="list-group-item" onclick="addTag($(this).html())" id="' + tag + '">' + tag + '</li>');
		}
        console.log("aaaa");
		$('#tagDialogTrigger').click();
        console.log("aaaa");
	});
};

function preview(){
	TagManager.markdown($('#blog_content').val(), function(content) {
		$("#preview_div").empty();
		$("#preview_div").append(content);
		$('#previewDialogTrigger').click();
	});
}

function blog_submit() {
	$.ajax({
		url: ".." + window.location.pathname,
		type: "POST",
		data: {
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
			date: $('#blog_date').val(),
			title: $('#blog_title').val(),
			content: $('#blog_content').val(),
			tags: JSON.stringify(TagManager.readTags('#selectedTag .tag'))
		}
	}).done(function(data) {
		alert(data);
		window.location.href = ".." + window.location.pathname;
	});
}

function deleteThis(self) {
	self.remove();
}
