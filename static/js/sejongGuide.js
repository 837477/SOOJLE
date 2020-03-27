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
					<div class="guide_subtitle noselect">
						세종대학교 통합 모바일 앱과 UCheck 앱을 설치할 수 있습니다!
					</div>
					<div class="guide_body noselect">
						<div class="guide_app_mobile_cont">
							<img src="static/image/app_guide.png" class="guide_app_mobile wow animated fadeInLeft">
						</div><div id="guide_app_container" class="guide_app_container">
							<a title="App Store" target="_blank" href="https://apps.apple.com/kr/app/%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90-%ED%86%B5%ED%95%A9-%EB%AA%A8%EB%B0%94%EC%9D%BC-%EC%95%B1/id1465703023?mt=8" style="overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2019-08-29&kind=iossoftware&bubble=apple_music) no-repeat center;" class="guide_app_link_btn_apple"></a>
							<a title="Play Store" target="_blank" class="sejongapp_btn" href='https://play.google.com/store/apps/details?id=kr.ac.sejong.smartcampus&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' class="guide_app_link_btn_google"></a>
						</div>
						<div style="position: relative; width:100%; height:50px;"></div>
						<div class="guide_app_mobile_cont">
							<img src="static/image/ucheck_guide.png" class="guide_app_mobile wow animated fadeInLeft">
						</div><div id="guide_app_container" class="guide_app_container">
							<a title="App Store" target="_blank" href="https://apps.apple.com/us/app/ucheck-plus/id1139582817?mt=8" style="overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2019-08-29&kind=iossoftware&bubble=apple_music) no-repeat center;" class="guide_app_link_btn_apple"></a>
							<a title="Play Store" target="_blank" class="sejongapp_btn" href='https://play.google.com/store/apps/details?id=com.libeka.attendance.ucheckplusstud'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' class="guide_app_link_btn_google"></a>
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
					<div class="guide_page_cont">
						<a target="_blank" href="http://www.sejong.ac.kr/unilife/guide.html" title="새내기 가이드">
							<img class="guide_page_icon" src="/static/image/logo_sejong.png">
						</a>
						<a target="_blank" href="https://www.youtube.com/user/channelsejongUCC" title="세종대학교 공식 유튜브">
							<img class="guide_page_icon" src="/static/image/logo_youtube.png">
						</a>
						<a target="_blank" href="https://www.facebook.com/sejongpr" title="세종대학교 공식 페이스북 페이지">
							<img class="guide_page_icon" src="/static/image/logo_facebook.png">
						</a>
						<a target="_blank" href="https://www.instagram.com/sejong_univ/" title="세종대학교 공식 인스타그램">
							<img class="guide_page_icon" src="/static/image/logo_instagram.png">
						</a>
						<a target="_blank" href="https://blog.naver.com/sejong_univ" title="세종대학교 공식 블로그">
							<img class="guide_page_icon" src="/static/image/logo_naverblog.png">
						</a>
						<div class="guide_page_icon_span">
							PC기준 책갈피, Mobile기준 우측하단 메뉴를 통해서 더 많은 사이트를 만날 수 있습니다.
						</div>
					</div>

					<div class="guide_title noselect">캠퍼스 둘러보기</div>
					<div class="guide_subtitle noselect">
						세종대학교 캠퍼스 내 건물의 위치를 확인하세요!
					</div>
					<div class="guide_body noselect">
						<a href="/static/image/sejong_campus.jpg" target="_blank" title="크게 보기">
							<img src="/static/image/sejong_campus.jpg" class="guide_campus_map wow animated zoomIn">
						</a>
						<div id="guide_campus_search_cont" class="guide_campus_search_cont">
							<input type="text" id="guide_campus_search" class="guide_campus_search" placeholder="장소를 검색해주세요." maxlength="50"></input
							><div class="guide_campus_search_btn pointer">
								<img src="/static/icons/search.png" class="guide_campus_search_icon">
							</div>
						</div>
					</div>
					<div class="guide_line"></div>
					</div>
				`;
	target.append(div);

	guide_campus_search_event();	// 캠퍼스 장소 검색 이벤트 바인딩

	$("#mobile_controller_none").addClass("display_none");
	$("#board_loading_modal").addClass("board_loading_modal_unvisible");
	$(".mobile_controller").removeAttr("style");
	$("#none_click").addClass("display_none");

	$("#menu_container").removeClass("menu_container_fixed");
	$("#posts_creating_loading").addClass("display_none");
	$("#board_container").removeClass("board_container_fixed");
}



function guide_campus_search_event() {
	$("#guide_campus_search").on({
		"focus": ()=> {
			$("#guide_campus_search_cont").css("border", "2px solid #12b886");
		},
		"blur": ()=> {
			$("#guide_campus_search_cont").removeAttr("style");
		}
	});
}