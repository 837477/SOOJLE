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
	// OFFICE 365
	// 인터넷 증명서
	let target = $("#posts_target");
	let div = 	`
					<div class="guide_title noselect">앱 설치하기</div>
					<div class="guide_subtitle noselect">
						세종대학교 통합 모바일 앱과 UCheck 앱을 설치할 수 있습니다!
					</div>
					<div class="guide_body guide_body_first noselect">
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
							<input type="text" id="guide_campus_search" class="guide_campus_search" placeholder="장소를 검색해주세요." maxlength="50" onkeyup="guide_campus_search_input()"></input
							><div class="guide_campus_search_btn pointer">
								<img src="/static/icons/search.png" class="guide_campus_search_icon">
							</div>
						</div>
						<div id="guide_campus_search_result_cont" class="guide_campus_search_result_cont"></div>
						<div class="guide_page_icon_span">
							더 추가하실 장소가 있나요?
							<a href="/board#feedback">피드백</a>을 해주세요!
						</div>
					</div>
					<div class="guide_line"></div>
					</div>
				`;
	target.append(div);

	guide_campus_search_event();	// 캠퍼스 장소 검색 이벤트 바인딩
	guide_campus_search_input();	// 캠퍼스 장소 검색 결과 
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
function guide_campus_search_input() {
	$("#guide_campus_search_result_cont").empty();
	let target = $("#guide_campus_search_result_cont");
	let text = $("#guide_campus_search").val();
	if (text == '') {
		target.append(`<img class="guide_campus_search_none noselect" src="/static/image/shortcut.jpg">`);
	} else {
		for (let spot in CAMPUS) {
			if (spot.toUpperCase().match(text.toUpperCase())) {
				target.append(`<div class="guide_campus_search_result">${spot}</div>`);
				for (let place of CAMPUS[spot]) {
					let spot2 = place.slice(0, place.indexOf('[')-1) + '<span style="color:#0071e3">' + place.slice(place.indexOf('[')-1, place.length) + '</span>';
					target.append(`<div class="guide_campus_search_result">${spot} - ${spot2}</div>`);
				}
				continue;
			} else {
				for (let place of CAMPUS[spot]) {
					if (place.toUpperCase().match(text.toUpperCase())) {
						let spot2 = place.slice(0, place.indexOf('[')-1) + '<span style="color:#0071e3">' + place.slice(place.indexOf('[')-1, place.length) + '</span>';
						target.append(`<div class="guide_campus_search_result">${spot} - ${spot2}</div>`);
					}
				}
			}
		}
	}
}


// 세종가이드 장소 목록
const CAMPUS = {
	'무방관': [],
	'세종초등학교': [],
	'홍진구조실험센터': [],
	'평생교육원 별관': [],
	'용덕관': [],
	'영실관': [],
	'주차빌딩': [],
	'충무관': 
		[
			'복사실 [1F]',
			'카페딕셔너리(카페) [1F]'
		],
	'진관홀': 
		[
			'학식 [B1]',
			'매점 [B1]'
		],
	'우정당': 
		[
			'학식 [1F]',
			'GS25편의점 [1F]',
			'브리클린(카페) [1F]'
		],
	'다산관': 
		[
			'ROTC 사무실 [3F]'
		],
	'광개토관': 
		[
			'국제교육원 [9F]',
			'복사실 [1F]',
			'GS25편의점 [B1]',
			'컨벤션센터 [B2]',
			'컨벤션홀 [B2]',
			'그라찌에(카페) [B1]',
			'소극장 [15F]',
			'게스트하우스 [14F]',
			'전시실 [B1]',
			'카페514(카페) [5F]'
		],
	'율곡관': 
		[
			'GS25편의점 [B1]'
		],
	'이당관': [],
	'군자관': 
		[
			'군자의밥상 [6F]',
			'학식 [B1]',
			'매점 [B1]',
			'대학서점 [1F]',
			'복사실 [1F]',
			'우리은행 [1F]',
			'우체국 [1F]',
			'사진관 [1F]',
			'안경점 [1F]',
			'여행사 [1F]'
		],
	'집현관': 
		[
			'비서실 [10F]',
			'법무감사실 [3F]',
			'홍보실 [2F]',
			'세종나눔봉사단 [1F]',
			'재무과 [2F]',
			'기획처 [2F]',
			'교무과 [1F]',
			'입학과 [2F]',
			'학생지원과 [1F]',
			'연구지원과 [2F]',
			'총무과 [1F]',
			'구매과 [1F]',
			'건설개발과 [1F]',
			'재산관리과 [1F]',
			'세종한국어문화교육센터 [9F]',
			'GM센터 [5F]',
			'보건실 [1F]'
		],
	'애지헌': 
		[
			'교목실 [B1]'
		],
	'박물관': 
		[
			'민속실 [2F]',
			'의상실 [3F]',
			'소형목공예실 [4F]',
			'대형목공예실 [5F]'
		],
	'대양AI센터': 
		[
			'미래교육원 [3F]',
			'콜라보랩 [3F]',
			'주차장 [B5~B3]',
			'조리실습실 [B2]',
			'글로벌지식평생교육원 [B2]',
			'전산실습실 [B2~B1]',
			'투썸(카페) [1F]',
			'세종스포츠정형외과 [1F]',
			'CU편의점 [1F]',
			'빅베어8 [2F]',
			'게스트하우스 [9F~11F]',
			'회의실 [12F]',
			'샤워실 [B2]',
			'약국 [1F]'
		],
	'모짜르트홀': [],
	'대양홀': 
		[
			'연습실 [5F]',
			'대강당 [1F~4F]',
			'공연장 [1F~4F]',
			'이발소 [B1]'
		],
	'세종관': [],
	'동천관(학술정보원)': 
		[
			'자료실 [5F~6F, 9F]',
			'자유열람실 [3F, 8F]',
			'스터디룸 [4F, 7F]',
			'창의토론라운지 [4F]',
			'전산실습실 [4F]',
			'교수학습개발센터 [4F]',
			'독서당 [4F]',
			'교양영어테스트센터 [4F]',
			'인터넷라운지 [3F]',
			'노트북전용석 [3F]',
			'특정반스터디룸 [3F]',
			'대출실 [2F]',
			'전자정보실 [2F]',
			'학술정보실 [2F]',
			'A/B/C자유열람실 [1F]',
			'카페드림(카페) [1F]',
			'D자유열람실 [B1]',
			'보존서고 [B2]'
		],
	'운동장': 
		[
			'농구장'
		],
	'아사달연못': [],
	'학생회관': 
		[
			'동아리방 [5F~6F]',
			'총학생회 [4F]',
			'단과대학생회 [4F]',
			'예비역협의회 [4F]',
			'동아리연합회 [4F]',
			'학생생활상담소 [3F]',
			'취업지원과 [3F]',
			'현장실습지원센터 [3F]',
			'창업지원센터 [3F]',
			'세종라운지 [3F]',
			'Global Lounge [2F]',
			'국제교류센터 [2F]',
			'대외협력처 [2F]',
			'제주몰빵 [2F]',
			'암벽등반장 [2F]',
			'파리바게트 [1F]',
			'CU편의점 [1F]',
			'미스사이공 [1F]',
			'석관동떡볶이 [1F]',
			'리얼후라이 [1F]',
			'팬도로시(카페) [1F]',
			'학식 [B1]',
			'소공연장 [B1]',
			'대공연장 [B1]',
			'동아리연습실 [B2]',
			'헬스장 [B2]',
			'샤워실 [B2]',
			'수업과 [2F]',
			'학적과 [2F]',
			'교직과 [2F]'
		],
	'교문': [],
	'쪽문': [],
	'후문': [],
	'새날관(행복기숙사)':
		[
			'생활지도실 [3F]',
			'행정실 [3F]',
			'세미나실 [3F]',
			'세탁실 [3F]',
			'휴게실 [1F]',
			'우편실 [1F]',
			'무인택배보관실 [1F]',
			'학식 [B1]',
			'샤워실 [B1]',
			'주차장 [B1]',
			'자전거보관소 [후문]',
			'카페 [B1]'
		],
	'주차타워': [],
	'캠퍼스타운': [],
	'흡연장': []
}