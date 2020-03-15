// URL Detection
window.addEventListener('hashchange', function() {
	URL_Select();
});
function URL_Detection() {
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	$("#pc_search_input").val("");
	$("#mobile_search_input").val("");

	$("#mobile_controller_none").addClass("display_none");
	$("#board_loading_modal").addClass("board_loading_modal_unvisible");
	$(".mobile_controller").removeAttr("style");
	$("#none_click").addClass("display_none");

	$("#menu_container").removeClass("menu_container_fixed");
	//$("#menu_container").removeAttr("style");
	$("#posts_creating_loading").addClass("display_none");
	$("#board_container").removeClass("board_container_fixed");

	URL_Select();
}
async function URL_Select() {
	let url_target = window.location.href.split("#")[1];
	if (url_target == undefined || url_target == "" || url_target == "recommend") {
		get_recommend_posts(1);
	}
	else if (url_target.startsWith("search?")) {
		let text = decodeURI(window.location.href);
		text = text.split("#search?")[1];
		text = text.split("/")[0];
		text = text.replace(/\+/g, " ");
		await search_text(text);
	}
	else if (url_target == "license") Insert_license();
	else if (url_target == "privacy") Insert_privacy();
	else if (url_target == "recommend") get_recommend_posts(1);
	else if (url_target == "popularity") {
		menu_open = 1;
		get_popularity_posts();
	}
	else if (url_target == "userlike") {
		menu_open = 1;
		get_user_like_posts();
	}
	else if (url_target == "userview") {
		menu_open = 1;
		get_user_view_posts();
	}
	else if (url_target.startsWith("topic?")) {
		menu_open = 1;
		let text = decodeURI(window.location.href);
		let target_topic = text.split("topic?")[1];
		get_topic_posts(target_topic);
	}
	else if (url_target == "lab") {
		menu_open = 1;
		Go_lab();
	}
	else if (url_target == "analysistics") {
		menu_open = 1;
		Go_analysistic();
	}
	else if (url_target == "setting") {
		menu_open = 1;
		Go_setting();
	}
	else if (url_target == "feedback") {
		menu_open = 1;
		Go_feedback();
	}
	else if (url_target == "soojle") {
		Go_management();
	}
	else if (url_target == "signinup") {
		get_recommend_posts(1);
		Login_open();
	}
	else if (url_target.startsWith("dvnote")) {
		menu_open = 1;
		Go_dvnote();
	}
	// Else : Nothing Do.
}
//----------------------------------------------------------------------------------
function Go_introduce() {
	//window.location.href = "/introduce";
	location.href = "/introduce";
}
function Go_programmer() {
	//window.location.href = "/programmer";
	location.href = "/programmer";
}
function Go_advertisement() {
	//window.location.href = "/advertisement";
	location.href = "/advertisement";
}
function Go_privacy() {
	//window.location.href = "/board#privacy";
	location.replace("/board#privacy");
	URL_Select();
}
function Go_license() {
	//window.location.href = "/board#license";
	location.replace("/board#license");
	URL_Select();
}
//----------------------------------------------------------------------------------
function Insert_license() {
	out_of_search();
	now_topic = "License";
	where_topic = "License";
	now_state = "License";
	let now_creating_state = now_state;		// 이거 중요함. 안 겹치게 함.
	$("#board_info_board").text("LICENSE");
	$("#board_info_text").text("오픈 라이센스");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);

	let div = 	`<div class="lab_title_wrap">
					<div class="lab_title noselect">라이센스</div>
					<div class="lab_subtitle noselect">
						다음은 SOOJLE의 중요한 부분을 담당하는 소스코드의 라이센스입니다.
					</div>
				</div>
				<div class="license_block">${license_1}</div>
				<div class="license_block">${license_2}</div>
				<div class="license_block">${license_3}</div>
				<div class="license_block">${license_4}</div>
				`;
	$("#posts_target").append(div);
	$("#posts_creating_loading").addClass("display_none");
}


function Insert_privacy() {
	out_of_search();
	now_topic = "Privacy";
	where_topic = "Privacy";
	now_state = "Privacy";
	let now_creating_state = now_state;
	$("#board_info_board").text("SOOJLE");
	$("#board_info_text").text("개인정보처리방침");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);

	let div = 	`<div class="lab_title_wrap">
					<div class="lab_title noselect">개인정보처리방침</div>
					<div class="lab_subtitle noselect">
						다음은 SOOJLE 서비스의 개인정보처리방침입니다.
					</div>
					<div class="license_block">${privacy_1}</div>
				</div>`;
	$("#posts_target").append(div);
	$("#posts_creating_loading").addClass("display_none");
}



/*--------------<License Info>--------------*/
// ChartJS
let license_1 = `The MIT License (MIT)<br>Copyright (c) 2018 Chart.js Contributors<br>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:<br>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.<br>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.`;
// Animated CSS
let license_2 = `The MIT License (MIT)<br>Copyright (c) 2019 Daniel Eden<br>Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated documentation files (the "Software"), to dealin the Software without restriction, including without limitation the rightsto use, copy, modify, merge, publish, distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software isfurnished to do so, subject to the following conditions:<br>The above copyright notice and this permission notice shall be included in allcopies or substantial portions of the Software.<br>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THESOFTWARE.`;
// FontAwesome
let license_3 = `Font Awesome Free License<br>-------------------------<br>Font Awesome Free is free, open source, and GPL friendly. You can use it forcommercial projects, open source projects, or really almost whatever you want.Full Font Awesome Free license: https://fontawesome.com/license/free.<br># Icons: CC BY 4.0 License (https://creativecommons.org/licenses/by/4.0/)In the Font Awesome Free download, the CC BY 4.0 license applies to all iconspackaged as SVG and JS file types.`;
// JQUERY
let license_4 = `Copyright JS Foundation and other contributors, https://js.foundation/<br>Permission is hereby granted, free of charge, to any person obtaininga copy of this software and associated documentation files (the"Software"), to deal in the Software without restriction, includingwithout limitation the rights to use, copy, modify, merge, publish,distribute, sublicense, and/or sell copies of the Software, and topermit persons to whom the Software is furnished to do so, subject tothe following conditions:<br>The above copyright notice and this permission notice shall beincluded in all copies or substantial portions of the Software.<br>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OFMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE ANDNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BELIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTIONOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTIONWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.`;
/*--------------<Privacy Info>--------------*/
let privacy_service_name = `SOOJLE`;
let privacy_domain = `soojle.com`;
let privacy_officer_team = `TEAM IML`;
let privacy_officer_name = `신희재`;
let privacy_officer_position = `세종대학교 컴퓨터공학과`;
let privacy_officer_rank = `학부생`;
let privacy_officer_number = `01045793099`;
let privarcy_officer_email = `soojleteam@gmail.com`;
let privacy_1 = `<p><strong>1. 개인정보의 처리 목적</strong></p><p><em>(&#39;${privacy_domain}&#39;이하 &#39;${privacy_service_name}&#39;)</em> 은(는) 다음의 목적을 위하여 개인정보를 처리하고 있으며, 다음의 목적 이외의 용도로는 이용하지 않습니다.</p><p>- 고객 가입의사 확인, 고객에 대한 서비스 제공에 따른 본인 식별.인증, 회원자격 유지.관리, 물품 또는 서비스 공급에 따른 금액 결제, 물품 또는 서비스의 공급.배송 등</p><p>&nbsp;</p><p><strong>2. 개인정보의 처리 및 보유 기간</strong></p><p>① <em>(&#39;${privacy_domain}&#39;이하 &#39;${privacy_service_name}&#39;)</em> 은(는) 정보주체로부터 개인정보를 수집할 때 동의 받은 개인정보 보유․이용기간 또는 법령에 따른 개인정보 보유․이용기간 내에서 개인정보를 처리․보유합니다.</p><p>② 구체적인 개인정보 처리 및 보유 기간은 다음과 같습니다.</p><p>☞ 아래 예시를 참고하여 개인정보 처리업무와 개인정보 처리업무에 대한 보유기간 및 관련 법령, 근거 등을 기재합니다.</p><p>(예시) - 고객 가입 및 관리 : 서비스 이용계약 또는 회원가입 해지 시까지, 다만 채권․채무관계 잔존 시에는 해당 채권․채무관계 정산 시까지</p><p>- 전자상거래에서의 계약․청약철회, 대금결제, 재화 등 공급기록 : 5년</p><p>&nbsp;</p><p><strong>3. 개인정보의 제3자 제공에 관한 사항</strong></p><p>① <em>(&#39;${privacy_domain}&#39;이하 &#39;${privacy_service_name}&#39;)</em> 은(는) 정보주체의 동의, 법률의 특별한 규정 등 개인정보 보호법 제17조 및 제18조에 해당하는 경우에만 개인정보를 제3자에게 제공합니다.</p><p>② <em>(&#39;${privacy_domain}&#39;)</em>은(는) 다음과 같이 개인정보를 제3자에게 제공하고 있습니다.</p><div class="privacy_officer_info"><p> - 개인정보를 제공받는 자 : ${privacy_service_name}</p><p> - 제공받는 자의 개인정보 이용목적 : 로그인ID, 서비스 이용 기록, 접속 로그, 접속 IP 정보, 소속학과</p><p> - 제공받는 자의 보유.이용기간: 지체 없이 파기</p></div><p>&nbsp;</p><p><strong>4. 개인정보처리 위탁</strong></p><p>① <em>(&#39;${privacy_service_name}&#39;)</em> 은(는) 원활한 개인정보 업무처리를 위하여 다음과 같이 개인정보 처리업무를 위탁하고 있습니다.</p><p>② <em>(&#39;${privacy_domain}&#39;이하 &#39;${privacy_service_name}&#39;)</em> 은(는) 위탁계약 체결 시 개인정보 보호법 제25조에 따라 위탁업무 수행 목적 외 개인정보 처리 금지, 기술적․관리적 보호 조치, 재위탁 제한, 수탁자에 대한 관리․감독, 손해배상 등 책임에 관한 사항을 계약서 등 문서에 명시하고, 수탁자가 개인정보를 안전하게 처리하는지를 감독하고 있습니다.</p><p>③ 위탁업무의 내용이나 수탁자가 변경될 경우에는 지체 없이 본 개인정보 처리방침을 통하여 공개하도록 하겠습니다.</p><p>&nbsp;</p><p><strong>5. 정보주체와 법정대리인의 권리·의무 및 그 행사방법 이용자는 개인정보주체로써 다음과 같은 권리를 행사할 수 있습니다.</strong></p><p>① 정보주체는 ${privacy_officer_team}(‘${privacy_domain}’이하 ‘${privacy_service_name}’)에 대해 언제든지 다음 각 호의 개인정보 보호 관련 권리를 행사할 수 있습니다.</p><ol><li>개인정보 열람 요구</li><li>해당 서비스 정보를 통한 통계 정보 산출</li></ol><p>&nbsp;</p><p><strong>6. 처리하는 개인정보의 항목 작성</strong></p><p>① <em>(&#39;${privacy_domain}&#39;이하 &#39;${privacy_service_name}&#39;)</em> 은(는) 다음의 개인정보 항목을 처리하고 있습니다.</p><p>&nbsp;</p><p><strong>7. 개인정보의 파기(&#39;${privacy_service_name}&#39;)은(는) 원칙적으로 개인정보 처리 목적이 달성된 경우에는 지체 없이 해당 개인정보를 파기합니다. 파기의 절차, 기한 및 방법은 다음과 같습니다.</strong></p><ul><li>파기절차 이용자가 입력한 정보는 목적 달성 후 별도의 DB에 옮겨져(종이의 경우 별도의 서류) 내부 방침 및 기타 관련 법령에 따라 일정 기간 저장된 후 혹은 즉시 파기됩니다. 이때, DB로 옮겨진 개인정보는 법률에 의한 경우가 아니고서는 다른 목적으로 이용되지 않습니다.</li></ul><ul><li>파기 기한 이용자의 개인정보는 개인정보의 보유기간이 경과된 경우에는 보유기간의 종료일로부터 5일 이내에, 개인정보의 처리 목적 달성, 해당 서비스의 폐지, 사업의 종료 등 그 개인정보가 불필요하게 되었을 때에는 개인정보의 처리가 불필요한 것으로 인정되는 날로부터 5일 이내에 그 개인정보를 파기합니다.</li></ul><p>&nbsp;</p><p><strong>8. 개인정보 자동 수집 장치의 설치•운영 및 거부에 관한 사항</strong></p><p>① ${privacy_officer_team} 은 개별적인 맞춤 서비스를 제공하기 위해 이용정보를 저장하고 수시로 불러오는 ‘쿠키(cookie)’를 사용합니다.</p><p>② 쿠키는 웹사이트를 운영하는데 이용되는 서버(http 및 https)가 이용자의 컴퓨터 브라우저에게 보내는 소량의 정보이며 이용자들의 PC 컴퓨터 내의 하드디스크에 저장되기도 합니다. <span style="font-weight:bold">가.</span> 쿠키의 사용 목적 : 이용자가 방문한 각 서비스와 웹 사이트들에 대한 방문 및 이용 형태, 인기 검색어, 보안접속 여부, 등을 파악하여 이용자에게 최적화된 정보 제공을 위해 사용됩니다.  <span style="font-weight:bold">나.</span> 쿠키의 설치•운영 및 거부 : 웹브라우저 상단의 도구&gt;인터넷 옵션&gt;개인정보 메뉴의 옵션 설정을 통해 쿠키 저장을 거부할 수 있습니다.  <span style="font-weight:bold">다.</span> 쿠키 저장을 거부할 경우 맞춤형 서비스 이용에 어려움이 발생할 수 있습니다.</p><p>&nbsp;</p><p><strong>9. 개인정보 보호책임자 작성</strong></p><p>① ${privacy_officer_team}(‘${privacy_domain}’이하 ‘${privacy_service_name}’) 은(는) 개인정보 처리에 관한 업무를 총괄해서 책임지고, 개인정보 처리와 관련한 정보주체의 불만 처리 및 피해 구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.</p><p>▶ 개인정보 보호책임자</p><div class="privacy_officer_info"><p>성명 :${privacy_officer_name}</p><p>직책 :${privacy_officer_position}</p><p>직급 :${privacy_officer_rank}</p><p>연락처 :${privacy_officer_number}, <a href='mailto:${privarcy_officer_email}' target='_blank' class='url'>${privarcy_officer_email}</a>,</p><p>※ 개인정보 보호 담당부서로 연결됩니다.</p></div><p>② 정보주체께서는 ${privacy_officer_team}(‘${privacy_domain}’이하 ‘${privacy_service_name}’)의 서비스(또는 사업)을 이용하시면서 발생한 모든 개인정보 보호 관련 문의, 불만 처리, 피해 구제 등에 관한 사항을 개인정보 보호책임자 및 담당부서로 문의하실 수 있습니다. ${privacy_officer_team}(‘${privacy_domain}’이하 ‘SOOJLE) 은(는) 정보주체의 문의에 대해 지체 없이 답변 및 처리해드릴 것입니다.</p><p>&nbsp;</p><p><strong>10. 개인정보처리방침 변경</strong></p><p>① 이 개인정보처리방침은 시행 일로부터 적용되며, 법령 및 방침에 따른 변경 내용의 추가, 삭제 및 정정이 있는 경우에는 변경사항의 시행 7일 전부터 공지사항을 통하여 고지할 것입니다.</p><p>&nbsp;</p><p><strong>11. 개인정보의 안전성 확보 조치 (&#39;${privacy_service_name}&#39;)은(는) 개인정보보호법 제29조에 따라 다음과 같이 안전성 확보에 필요한 기술적/관리적 및 물리적 조치를 하고 있습니다.</strong></p><ol><li>해킹 등에 대비한 기술적 대책 &lt;<em>${privacy_officer_team}</em>&gt;(&#39;<em>${privacy_service_name}</em>&#39;)은 해킹이나 컴퓨터 바이러스 등에 의한 개인정보 유출 및 훼손을 막기 위하여 주기적인 갱신·점검을 하며 외부로부터 접근이 통제된 구역에 시스템을 설치하고 기술적/물리적으로 감시 및 차단하고 있습니다.</li><li>개인정보의 암호화 이용자의 개인정보는 비밀번호는 암호화되어 저장 및 관리되고 있어, 본인만이 알 수 있으며 중요한 데이터는 파일 및 전송 데이터를 암호화하거나 파일 잠금 기능을 사용하는 등의 별도 보안 기능을 사용하고 있습니다.</li><li>접속기록의 보관 및 위변조 방지 개인정보처리시스템에 접속한 기록을 최소 6개월 이상 보관, 관리하고 있으며, 접속 기록이 위변조 및 도난, 분실되지 않도록 보안 기능 사용하고 있습니다.</li><li>개인정보에 대한 접근 제한 개인정보를 처리하는 데이터베이스시스템에 대한 접근 권한의 부여, 변경, 말소를 통하여 개인정보에 대한 접근통제를 위하여 필요한 조치를 하고 있으며 침입차단시스템을 이용하여 외부로부터의 무단 접근을 통제하고 있습니다.</li></ol>`;
/*------------------------------------------*/