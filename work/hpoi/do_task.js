var a, b;
var option;
	console.log("hello world");
chrome.storage.sync.get({
	enable: false,
	reimage: false
}, function(items) {
	option = items;
	console.log(option);
	if (option.enable) {
		b = function() {
			$('.zm-item-vote').remove();
			$('.zm-votebar').remove();
			$('.zh-backtotop').remove();
			if (option.reimage){
				$('img').remove();
			}
		}
		a = function() {
			$('body').css("background-color", "black");
			$('body').css("color", "green");
			console.log(chrome.extension.getURL("sublime_top.png"));
			$('.zu-top').empty();
			$('.zu-top').css("background-image", 'url(' + chrome.extension.getURL("sublime_top.png") + ')');
			$('.zu-top').css("height", "41px");
			$('.zu-top').css("border", "0px");

			$('.zu-main').css("padding-left", "200px");
			$('.zu-main').before("<div class='qiuleft' style='width:200px;height:1272px;background-color:green;position:fixed'></div>");
			$('.qiuleft').css("background-image", 'url(' + chrome.extension.getURL("sublime_left.png") + ')');


			b();
		};
		a();
		setInterval(b, 1000);
	}
});