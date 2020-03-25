// 가이드 클릭
function Click_guide() {
	location.href = "/board#guide";
	menu_modal_onoff();
}

// 가이드 이동
function Go_guide() {
	let url_target = window.location.href.split("#")[1];
	out_of_search();
	now_topic = "대학가이드";
	where_topic = "대학가이드";
	now_state = "대학가이드";
	$("#board_info_board").text("SEJONG");
	$("#board_info_text").text("대학가이드");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);
	menu_modal_onoff();
	Insert_Sejong_Guide();
}

// 가이드 삽입
function Insert_Sejong_Guide() {
	let target = $("#posts_target");
	let div = 	`
					<div class="guide_title noselect">앱 설치하기</div>
					<div class="guide_body noselect">
						<div class="guide_app_mobile_cont">
							<img src="static/image/app_guide.png" class="guide_app_mobile wow animated fadeInLeft">
						</div><div id="guide_app_container" class="guide_app_container">
							<a title="App Store" target="_blank" href="https://apps.apple.com/kr/app/%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90-%ED%86%B5%ED%95%A9-%EB%AA%A8%EB%B0%94%EC%9D%BC-%EC%95%B1/id1465703023?mt=8" style="overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2019-08-29&kind=iossoftware&bubble=apple_music) no-repeat center;" class="guide_app_link_btn_apple"></a>
							<a title="Play Store" target="_blank" class="sejongapp_btn" href='https://play.google.com/store/apps/details?id=kr.ac.sejong.smartcampus&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' class="guide_app_link_btn_google"></a>
						</div>
					</div>
					<div class="guide_banner">
						<div class="circle-container">
					    	<div class="circle" style="background-color: #c30e2e;"></div>
						</div>
						<div class="circle-container">
							<div class="circle" style="background-color: #12b886;"></div>
						</div>
						<div class="circle-container">
							<div class="circle" style="background-color: #0071e3;"></div>
						</div>
					</div>
					
				`;
	// <div class="guide_title noselect">캠퍼스 안내도</div>
	// 				<div class="guide_body noselect">
	// 					<a target="_blank" href="static/image/sejong_campus.jpg" title="크게보기">
	// 						<img src="/static/image/sejong_campus.jpg" class="guide_campus_map">
	// 					</a>
	// 				</div>
	target.append(div);

	$("#mobile_controller_none").addClass("display_none");
	$("#board_loading_modal").addClass("board_loading_modal_unvisible");
	$(".mobile_controller").removeAttr("style");
	$("#none_click").addClass("display_none");

	$("#menu_container").removeClass("menu_container_fixed");
	$("#posts_creating_loading").addClass("display_none");
	$("#board_container").removeClass("board_container_fixed");
}




function Guide_Move_1() {
	$("html").animate({"scrollTop": $("#guide_app_container").offset().top - 100}, 400);
}