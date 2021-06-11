
/*function click(){
	target = $("body > div.container-fluid.hpoi-banner-box > div.container > div > div.col-md-6.hpoi-entry-margin > div.hpoi-entry-score-box > div.hpoi-entry-score-stars > div > div.rating-container.rating-gly-star");
	target.click();
	console.log(target);
	width = target.width();
	height = target.height();
	console.log(target.offset());
	p_top = target.offset().top;
	left = target.offset().left;
	x = left + width*0.9;
	y = p_top + height * 0.5;
	console.log(x);
	console.log(y);
	e = new jQuery.Event("click");
	e.pageX = x;
	e.pageY = y;
	console.log(target.trigger(e));
	$('body > div.container > div:nth-child(1) > div > div.swiper-container.swiper-gallery.swiper-container-initialized.swiper-container-horizontal > div > div.swiper-slide.imgWidth.swiper-slide-active > a > img').click();

}
click();
*/
console.log(data);
hobby_id = data['hobby_id'];
score = data['score'];
var r;
$.ajax({
	type : "POST",
	url : "hobby/rating/add/" + hobby_id,
	data : {'rating' : score},
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