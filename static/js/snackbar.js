function Snackbar(text) {
	let tag = $(document.createElement("div"));
	tag.addClass("snackbar noselect animated slideInUp");
	tag.attr({
		"onclick": "Snackbar_off($(this));",
		"data-wow-duration": "0.4s"
	});
	tag.text(text);
	$("#snackbar_target").append(tag);
	setTimeout(function() {
		Snackbar_off(tag);
	}, 4000);
}

function Snackbar_off(tag) {
	tag.removeClass("slideInUp");
	tag.addClass("slideOutDown");
	setTimeout(function() {
		tag.remove();
	}, 4000);
}