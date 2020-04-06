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
						세종대학교 필수 어플! 통합 모바일 앱과 UCheck 앱을 설치할 수 있습니다.
					</div>
					<div class="guide_body guide_body_first noselect">
						<div class="guide_app_mobile_cont">
							<img src="static/image/app_guide.png" class="guide_app_mobile wow animated fadeInLeft">
							<div id="guide_app_container" class="guide_app_container">
								<a title="App Store" target="_blank" href="https://apps.apple.com/kr/app/%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90-%ED%86%B5%ED%95%A9-%EB%AA%A8%EB%B0%94%EC%9D%BC-%EC%95%B1/id1465703023?mt=8" style="overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2019-08-29&kind=iossoftware&bubble=apple_music) no-repeat center;" class="guide_app_link_btn_apple"></a>
								<a title="Play Store" target="_blank" class="sejongapp_btn" href='https://play.google.com/store/apps/details?id=kr.ac.sejong.smartcampus&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' class="guide_app_link_btn_google"></a>
							</div>
						</div
						><div class="guide_app_mobile_cont">
							<img src="static/image/ucheck_guide.png" class="guide_app_mobile wow animated fadeInRight">
							<div id="guide_app_container" class="guide_app_container">
								<a title="App Store" target="_blank" href="https://apps.apple.com/us/app/ucheck-plus/id1139582817?mt=8" style="overflow:hidden;background:url(https://linkmaker.itunes.apple.com/en-us/badge-lrg.svg?releaseDate=2019-08-29&kind=iossoftware&bubble=apple_music) no-repeat center;" class="guide_app_link_btn_apple"></a>
								<a title="Play Store" target="_blank" class="sejongapp_btn" href='https://play.google.com/store/apps/details?id=com.libeka.attendance.ucheckplusstud'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' class="guide_app_link_btn_google"></a>
							</div>
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

					<div class="guide_title noselect">학생식당 영업시간</div>
					<div class="guide_subtitle noselect">
						세종대학교 캠퍼스 내 학생식당의 영업시간을 알아보세요!
					</div>
					<div class="guide_restaurnat_box_cont noselect">
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">학생회관 푸드코트</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								토요일: 10:30 ~ 14:00<br>
								(일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								토요일: 10:30 ~ 14:00<br>
								(일요일, 공휴일 휴무)
							</div>
						</div>
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">군자키친</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								(토,일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								(토,일요일, 공휴일 휴무)
							</div>
						</div>
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">진관키친</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								평일: 08:30 ~ 19:00<br>
								(토,일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								평일: 08:30 ~ 19:00<br>
								(토,일요일, 공휴일 휴무)
							</div>
						</div>
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">우정당 푸드코트</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								토요일: 10:00 ~ 14:00<br>
								(일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								휴무
							</div>
						</div>
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">군자의 밥상</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								점심: 11:30 ~ 14:00<br>
								저녁: 17:00 ~ 18:30<br>
								(토,일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								점심: 11:30 ~ 13:30<br>
								저녁: 17:00 ~ 18:00<br>
								(토,일요일, 공휴일 휴무)
							</div>
						</div>
						<div class="guide_restaurnat_box">
							<div class="guide_restaurnat_box_title">더큰도시락</div>
							<div class="guide_restaurnat_box_type">학기중</div>
							<div class="guide_restaurnat_box_post">
								평일: 09:00 ~ 19:00<br>
								토요일: 10:30 ~ 14:00<br>
								(일요일, 공휴일 휴무)
							</div>
							<div class="guide_restaurnat_box_type">방학중</div>
							<div class="guide_restaurnat_box_post">
								평일: 08:00 ~ 20:00<br>
								토요일: 08:00 ~ 20:00<br>
								(일요일, 공휴일 휴무)
							</div>
						</div>
					</div>
					<div class="guide_line"></div>
					</div>

					<div class="guide_title noselect">Office 365 서비스</div>
					<div class="guide_subtitle noselect">
						Office 365를 통해서 학교 업무와 각종 대학생 혜택을 누려보세요!
					</div>
					<div class="guide_office365_cont">
						<div class="guide_office365_svg animated wow slideInLeft">${Mail_Svg}</div>
						<div class="guide_office365_btn_cont noselect">
							<a target="_blank" href="http://o365.sejong.ac.kr/mysql/User/intro.jsp"><div class="guide_office365_btn pointer"><i class="fas fa-info-circle"></i> 안내</div></a>
							<a target="_blank" href="https://o365.sejong.ac.kr/mysql/User/login.jsp"><div class="guide_office365_btn pointer"><i class="fas fa-paper-plane"></i> 신청</div></a>
						</div>
						<div class="guide_office365_intro_cont">
							<div class="guide_office365_intro_title noselect">주요 기능</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">1. </span> 세종인을 위한 메일 계정 제공</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">2. </span> 50GB의 메일 사서함 제공</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">3. </span> One Drive: 1TB의 개인용 스토리지</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">4. </span> 최신 Office를 설치하여 사용 가능</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">5. </span> 학생인증 필요서비스 사용 가능</div>						
						</div
						><div class="guide_office365_intro_cont">
							<div class="guide_office365_intro_title noselect" style="color:#c30e2e">이용 안내</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">1. </span> 본 학교 신분이 아닐 시, 해당 학기 마지막일에 자동 탈퇴됩니다.</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">2. </span> 자동 탈퇴 처리 전에 백업을 완료해주십시오.</div>
							<div class="guide_office365_intro_post"><span class="guide_library_color_blue noselect">3. </span> 패스워드는 8자이상 권장합니다.(영문+숫자+특수문자)</div>				
						</div>
					</div>
					<div class="guide_line"></div>
					
					<div class="guide_title noselect">학술정보원 이용 안내</div>
					<div class="guide_subtitle noselect">
						학술정보원을 처음 이용하는 세종인을 위한 안내입니다.
					</div>
					<div class="guide_library_cont wow animated fadeInUp">
						<div class="guide_library_title noselect"><span class="guide_library_title_QnA">Q. </span>신입생인데 어떻게 열람실을 사용하나요?</div>
						<div class="guide_library_img_cont">
							<img class="guide_library_img" src="/static/image/logo_sejonglib.png">
							<div class="guide_library_info"><span class="guide_library_color_black noselect">1. </span><a target="_blank" href="https://library.sejong.ac.kr/index.ax">학술정보원 페이지</a>에 접속을 해줍니다.</div>
						</div
						><div class="guide_library_img_cont">
							<img class="guide_library_img" src="/static/image/btn_sejonglib.png">
							<div class="guide_library_info"><span class="guide_library_color_black noselect">2. </span>위 버튼을 찾아 클릭 후, 영상을 먼저 이수해주세요.</div>
						</div>
					</div>
					<div class="guide_library_cont wow animated fadeInUp">
						<div class="guide_library_title noselect"><span class="guide_library_title_QnA">Q. </span>자유열람실 이용제한은 어떻게 되나요?</div>
						<div class="guide_library_subtitle noselect">자유열람실 이용제한</div>
						<div class="guide_office365_intro_post"><span class="guide_library_color_red noselect">1. </span>제적, 정학, 자퇴, 면직, 학점교류 학생일 시, 이용 불가합니다.</div>
						<div class="guide_office365_intro_post"><span class="guide_library_color_red noselect">2. </span>대리발권 적발 시, 30일 이용 불가합니다.</div>
						<div class="guide_office365_intro_post"><span class="guide_library_color_red noselect">3. </span>열람실 미반납 3회 확인 시, 5일 이용 불가합니다.</div>
					</div>
					<div class="guide_library_cont wow animated fadeInUp">
						<div class="guide_library_title noselect"><span class="guide_library_title_QnA">Q. </span>학술정보원 사용시간은 어떻게 되나요?</div>
						<div class="guide_library_answer_box_cont noselect">
							<div class="guide_library_answer_box">
								<div class="guide_restaurnat_box_title">대출실 및 자료실</div>
								<div class="guide_restaurnat_box_type">학기중</div>
								<div class="guide_restaurnat_box_post">평일: 09:00 ~ 22:00<br>
								토요일: 09:00 ~ 17:00</div>
								<div class="guide_restaurnat_box_type">방학중</div>
								<div class="guide_restaurnat_box_post">09:00 ~ 17:00</div>
							</div
							><div class="guide_library_answer_box">
								<div class="guide_restaurnat_box_title">자유열람실</div>
								<div class="guide_restaurnat_box_type">학기중</div>
								<div class="guide_restaurnat_box_post">24시간</div>
								<div class="guide_restaurnat_box_type">방학중</div>
								<div class="guide_restaurnat_box_post">24시간</div>
							</div>
						</div>
					</div>
					<div class="guide_library_link_cont">
						<div class="guide_library_link"><a target="_blank" href="https://library.sejong.ac.kr/bbs/Detail.ax?bbsID=3&articleID=16">이용자 교육 FAQ</a></div
						><div class="guide_library_link"><a target="_blank" href="https://library.sejong.ac.kr/bbs/Detail.ax?bbsID=3&articleID=19">스터디룸 이용 FAQ</a></div>
					</div>
					<div class="guide_line"></div>

					<div class="guide_title noselect">꿀팁 8계명</div>
					<div class="guide_subtitle noselect">
					</div>
					<div class="guide_tip_cont">
						<div class="guide_tip"><span class="guide_library_color_green noselect">1. </span>일찍 일어나는 새(오전수업)가 성적을 잘 딴다.</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">2. </span>고전독서는 최대한 빨리 끝내버리자.</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">3. </span>소기코, 컴기코는 1학년 때 끝내는 것이 속 편하다.</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">4. </span>따로 계획이 없다면 군대는 빨리 가자.</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">5. </span>졸업 가능 요건 충족은 빠를 수록 좋다.</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">6. </span>봉사를 한다면 한번에 확실하게 끝내자!</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">7. </span>영어는 졸업 직전까지 함께한다..</div>
						<div class="guide_tip"><span class="guide_library_color_green noselect">8. </span>SOOJLE을 잘 활용하자! :)</div>
					</div>
					<div class="guide_line"></div>

					<div class="guide_page_icon_span noselect">
						본 페이지의 모든 정보는 언제든지 변경될 수 있으며, 만약 잘못된 정보는 <a href="/board#feedback">피드백</a>을 통해서 알려주세요!
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
	'용덕관': 
		[
			'다용도체육관 [4F]'
		],
	'영실관': [],
	'주차빌딩': [],
	'충무관': 
		[
			'복사실 [1F]',
			'카페딕셔너리(카페) [1F]'
		],
	'진관홀': 
		[
			'진관키친(학식) [B1]',
			'매점 [B1]'
		],
	'우정당': 
		[
			'푸드코트(학식) [1F]',
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
			'군자키친(학식) [B1]',
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
			'총장실 [10F]',
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
			'교목실 [B1]',
			'예배실 [1F]',
			'성가대실 [2F]'
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
			'전산정보실 [2F]',
			'학술정보실 [2F]',
			'멀티미디어실 [2F]',
			'A/B/C자유열람실 [1F]',
			'카페드림(카페) [1F]',
			'D자유열람실 [B1]',
			'보존서고 [B2]',
			'남학생휴게실 [B1]',
			'여학생휴게실 [7F]'
		],
	'운동장': 
		[
			'농구장 [야외]'
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
			'푸드코트(학식) [B1]',
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
			'더큰도시락(학식) [B1]',
			'샤워실 [B1]',
			'주차장 [B1]',
			'자전거보관소 [후문]',
			'카페 [B1]'
		],
	'주차타워': [],
	'캠퍼스타운': [],
	'흡연장': []
}
// 메일 SVG
const Mail_Svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 513 222">
  <g id="그룹_15" data-name="그룹 15" transform="translate(-3029 2716)">
    <g id="그룹_14" data-name="그룹 14" transform="translate(388 -40)">
      <g id="빼기_1" data-name="빼기 1" transform="translate(2803.849 -2763.172)" fill="none">
        <path d="M238.152,285.172h-222a16,16,0,0,1-16-16v-137a16,16,0,0,1,16-16h2c.09.093.183.187.277.281l97.531,91.587c4.819,4.819,8.66,6.969,12.452,6.969,3.75,0,7.572-2.149,12.391-6.969l89.555-85.782a21.987,21.987,0,0,0,4.306-6.086h3.484a16,16,0,0,1,16,16v137a16,16,0,0,1-16,16Z" stroke="none"/>
        <path d="M 238.1516876220703 277.1722412109375 C 240.2883911132813 277.1722412109375 242.2971801757813 276.3401489257813 243.8079681396484 274.8293151855469 C 245.3188934326172 273.3183288574219 246.1510162353516 271.3091735839844 246.1510162353516 269.1719970703125 L 246.1510162353516 132.1722412109375 C 246.1510162353516 130.0353240966797 245.3188934326172 128.0262908935547 243.8079376220703 126.5152053833008 C 242.5344390869141 125.2416458129883 240.9072113037109 124.450325012207 239.1480255126953 124.2330551147461 C 238.1883239746094 125.5596237182617 237.1067352294922 126.8255081176758 235.8960571289063 128.0350799560547 L 146.4636383056641 213.6963653564453 C 142.1281890869141 218.0317840576172 136.1587677001953 223.0082092285156 128.4156036376953 223.0082092285156 C 120.6181411743164 223.0082092285156 114.6417694091797 218.0317840576172 110.4868469238281 213.8712921142578 L 15.07556438446045 124.2432708740234 C 13.34668159484863 124.4743041992188 11.74904441833496 125.2609329223633 10.49460029602051 126.5154113769531 C 8.983433723449707 128.0265350341797 8.151183128356934 130.0355377197266 8.151183128356934 132.1722412109375 L 8.151183128356934 269.1719970703125 C 8.151183128356934 271.3089599609375 8.983391761779785 273.3180236816406 10.49447536468506 274.8290710449219 C 12.00555896759033 276.340087890625 14.01455879211426 277.1722412109375 16.15143394470215 277.1722412109375 L 238.1516876220703 277.1722412109375 M 238.1516876220703 285.1722412109375 L 16.15143394470215 285.1722412109375 C 11.87768363952637 285.1722412109375 7.859766960144043 283.5079650878906 4.837725162506104 280.4860229492188 C 1.815558433532715 277.4639587402344 0.1511834859848022 273.4459228515625 0.1511834859848022 269.1719970703125 L 0.1511834859848022 132.1722412109375 C 0.1511834859848022 127.8986206054688 1.815558433532715 123.8806991577148 4.837725162506104 120.8585357666016 C 7.859891891479492 117.8363723754883 11.87780857086182 116.1719970703125 16.15143394470215 116.1719970703125 L 18.155517578125 116.1719970703125 C 18.24568367004395 116.2648696899414 18.33843421936035 116.3592834472656 18.43201637268066 116.4528274536133 L 115.9631805419922 208.0394897460938 C 120.7826385498047 212.8589477539063 124.6231384277344 215.0082092285156 128.4156036376953 215.0082092285156 C 132.1657257080078 215.0082092285156 135.9873046875 212.8589477539063 140.8068084716797 208.0394897460938 L 230.3622283935547 122.2578277587891 C 232.1398010253906 120.4800338745117 233.5884399414063 118.4324951171875 234.6678009033203 116.1719970703125 L 238.1516876220703 116.1719970703125 C 242.4252319335938 116.1719970703125 246.4430236816406 117.8363723754883 249.4649810791016 120.8585357666016 C 252.4868011474609 123.8806228637695 254.1510162353516 127.8985748291016 254.1510162353516 132.1722412109375 L 254.1510162353516 269.1719970703125 C 254.1510162353516 273.446044921875 252.4868011474609 277.4640502929688 249.4649810791016 280.4860229492188 C 246.4431457519531 283.5079650878906 242.4253540039063 285.1722412109375 238.1516876220703 285.1722412109375 Z" stroke="none" fill="#12b886"/>
      </g>
      <line id="선_12" data-name="선 12" x2="220" transform="translate(2819.5 -2643)" fill="none" stroke="#12b886" stroke-linecap="round" stroke-width="8"/>
    </g>
    <line id="선_13" data-name="선 13" x2="86" transform="translate(3094.5 -2649.5)" fill="none" stroke="#12b886" stroke-linecap="round" stroke-width="5"/>
    <line id="선_14" data-name="선 14" x2="132" transform="translate(3048.5 -2609.5)" fill="none" stroke="#12b886" stroke-linecap="round" stroke-width="5"/>
    <line id="선_15" data-name="선 15" x2="84" transform="translate(3096.5 -2565.5)" fill="none" stroke="#12b886" stroke-linecap="round" stroke-width="5"/>
    <g id="타원_7" data-name="타원 7" transform="translate(3488 -2716)" fill="none" stroke="#0071e3" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_10" data-name="타원 10" transform="translate(3482 -2609)" fill="none" stroke="#c30e2e" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_11" data-name="타원 11" transform="translate(3468 -2675)" fill="none" stroke="#c30e2e" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_13" data-name="타원 13" transform="translate(3075 -2659)" fill="none" stroke="#12b886" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_14" data-name="타원 14" transform="translate(3029 -2619)" fill="none" stroke="#12b886" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_15" data-name="타원 15" transform="translate(3076 -2575)" fill="none" stroke="#12b886" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_12" data-name="타원 12" transform="translate(3517 -2557)" fill="none" stroke="#c30e2e" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_8" data-name="타원 8" transform="translate(3522 -2629)" fill="none" stroke="#0071e3" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
    <g id="타원_9" data-name="타원 9" transform="translate(3468 -2514)" fill="none" stroke="#0071e3" stroke-width="5">
      <circle cx="10" cy="10" r="10" stroke="none"/>
      <circle cx="10" cy="10" r="7.5" fill="none"/>
    </g>
  </g>
</svg>`;