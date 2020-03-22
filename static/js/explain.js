// 설명 시작할지 Check
setTimeout(function() {Check_Explain_Run();}, 1000);
function Check_Explain_Run() {
	let item = localStorage.getItem('sj-run');
	if (item != null && item != undefined && item != 'undefined') {
		return;
	} else {
		$("html").scrollTop(0);
		$("body").css("overflow", "hidden");
		Go_Soojle_Explain();
	}
}

// 설명 시작
function Go_Soojle_Explain() {
	//localStorage.setItem('sj-run', 'true');
	$("#soojle_explain").removeClass("display_none");
	let div = 	`
					<div>
						
					</div>
				`;
}

// 설명 나가기
function Exit_Soojle_Explain() {
	$("body").removeAttr("style");
	$("#soojle_explain").addClass("display_none");
}