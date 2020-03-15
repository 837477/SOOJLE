// Mobile Device Checked====================================================
window.mobilecheck = function() {
	var isMobile = false;
	if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
	    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
	    isMobile = true;
	}
    return isMobile;
};
// 호출: mobilecheck();


// 메인페이지 검색===========================================================
$("#pc_search_input").on({
	"focus": function() {
		searching_focus();
	}
})
$("#pc_search_input").focusout(() => {
	search_blur();
})
function searching_focus() {
	target = $("#search_recommend_box");
	if (mobilecheck()) {
		mobile_search_modal_open();
		target = $("#mobile_search_recommend_box");
	} else {
		$("#search_recommend_box").removeClass("display_none");
	}
	// 최근 검색어 표출
	Insert_user_recently_searchword(target);
}
let search_cache = "";	// 이전 검색어
let search_target = "";	// 목표 검색어
let now = 0;			// 현재 화살표로 선택한 div 위치
let all = 0;			// 검색결과 수
let search_open = 0; 	// 검색 모달 Open 여부
function search_focus(keyCode, tag) {
	if (mobilecheck() && search_open == 0) {
		mobile_search_modal_open();
		return;
	}
	if (!mobilecheck())
		$("#search_recommend_box").removeClass("display_none");
	if (keyCode == 13) {							// 엔터일 떄
		search_button();
		search_blur();
	} else if (keyCode == 38 || keyCode == 40) {	 // 방향키 일때 (위, 아래)
		$(`.search_result:nth-child(${now})`).removeClass("search_target");
		if (keyCode == 38) now--;
		else now++;

		if (now > $('.search_result').length) {
			now--;
		} else if (now < 0) {
			now++;
		}

		$(`.search_result:nth-child(${now})`).addClass("search_target");
		let target;
		if (mobilecheck()) {
			target = $(`#mobile_search_recommend_box > .search_result:nth-child(${now})`).text().trim();
		} else {
			target = $(`#search_recommend_box > .search_result:nth-child(${now})`).text().trim();
		}
		tag.val(target);
		search_cache = target;
	} else {
		let now_search = tag.val();
		// 문열길이!=0, 문자열변화
		if (now_search.length != 0 && search_cache != now_search) {
			$(`.search_result:nth-child(${now})`).removeClass("search_target");
			now = 0;
			search_cache = tag.val();
			search_target = search_cache;
			/*추천검색어 =========================================*/
			Insert_recommendation_searchword();
		} else if (tag.val() == "") {
			search_target = "";
			if (mobilecheck()) {
				$(".search_result").remove();
			} else {
				$("#search_recommend_box").addClass("display_none");
				$(".search_result").remove();
			}
			search_cache = "";
		}
	}
}
function mobile_search_modal_open() {
	if (search_open == 0) {
		if (mobilecheck()) {
			scroll(0,0);
			$("#mobile_search_modal").removeClass("display_none");
			$("#board_logo").css({"left": "10px",
								"transform": "translate(0, 0)",
								"-webkit-transform": "translate(0, 0)"})
			$("body").css("overflow", "hidden");
			$("#mobile_search_input").focus();
			search_open = 1;
		}
	} else {
		search_blur();
	}
}
function search_button() {	// 검색작업 data = 글자
	let data;
	if (mobilecheck()) {
		data = $("#mobile_search_input").val();
		$("#mobile_search_input").blur();
		$("#pc_search_input").val(data);
		search_blur();
		$("body").removeAttr("style");
		search_open = 0;
	} else {
		data = $("#pc_search_input").val();
		$("#pc_search_input").blur();
	}
	if (data == ""){
		Snackbar("검색어를 입력해주세요.");
		is_searching = 0;
		return;
	} else if (data.length > 200) {
		data = data.slice(0, 200);
	}
	search_text(data);	// 검색 함수 실행

	/*search 클릭 작업============================================================*/
}
function search_result_click(tag) {
	let data = tag.children("span").text().trim();
	if (mobilecheck()) {
		$("#mobile_search_input").val(data);
	} else {
		$("#pc_search_input").val(data);
	}
	search_button();
}
function search_blur() {
	$("#search_recommend_box").addClass("display_none");
}
function search_text(text) {
	if (text == "") {
		Snackbar("검색어를 입력해주세요.");
		return;
	}
	text = text.replace(/ /g, "+");
	window.location.href = "/board#search?" + text + '/'
}


// 페이지 이동 버튼==========================================================
function Gohome(){ window.location.href = "/"; }
function Goboard() { window.location.href = "/board"; }
function GoLogin() { window.location.href = "/board#signinup"; }
function GoSetting() { window.location.href = "/board#setting"; }
function Go_Recommend() { window.location.href = "/board#recommend"; }
function Go_Popularity() { window.location.href = "/board#popularity"; }
function Go_College() { window.location.href = "/board#topic?대학교"; }
function Go_Club() { window.location.href = "/board#topic?동아리&모임"; }
function Go_Contest() { window.location.href = "/board#topic?공모전&행사"; }
function Go_Job() { window.location.href = "/board#topic?진로&구인"; }


setTimeout(function() {
	$("body").removeAttr("style");
	$("#loading").addClass("display_none");
}, 0);


// 메인 페이지 설명 스크롤===================================================
function next_page(n) {
	let target = $(`.page_section:nth-child(${n})`).offset().top;
	$('html,body').animate({scrollTop: target}, 10);
}
function last_page() {
	let target = $("#last_blank").offset().top;
	$('html,body').animate({scrollTop: target}, 10);
}


// 메인 페이지 로그인=========================================================
$(window).ready(function() {
	token = localStorage.getItem('sj-state');
	if (token != null && token != undefined && token != 'undefined') {
		sessionStorage.setItem('sj-state', token);
	}
	Get_UserInfo(function(result) {	// result == 유저정보
		if (result) {
			$("#main_user_btn").css("color", "#12b886");
			$("#main_user_btn").text(result['user_nickname']+'');
			$("#main_user_btn").removeClass("display_none");
			$("#main_login_btn").addClass("display_none");
		}
	});
});


// 사용자 검색 키워드 객체
const user_recently_searchword = {
	search_list: [],
	setter: () => {
		Get_recently_searchword(function(result) {
			let output = []
			for (let i = 0; i < result.length; i++) {
				let is_possible = true;
				for (let j = i - 1; j >= 0; j--) {
					if (result[i]['original'] == result[j]['original']){
						is_possible = false;
						break;
					}
				}
				if (is_possible) {
					output.push(result[i]);
				}
			}
			this.search_list = output.splice(0,5).reverse();
		});
	},
	getter: () => {
		return this.search_list;
	}
}
user_recently_searchword.setter();

// 사용자 최근 검색어 넣기
function Insert_user_recently_searchword(target) {
	target.empty();
	let div = ``;
	let output = user_recently_searchword.getter();
	for (let search_word of output) {
		div = 	`
					<div class="search_result noselect" onmousedown="search_result_click($(this))">
						<img src="/static/icons/time.png" class="search_result_icon">
						<span class="text_overflow_none">${search_word['original']}</span>
					</div>
				`;
		target.prepend(div);
	}
	if (output.length == 0) {
		$.when(A_JAX(host_ip+"/get_search_realtime", "GET", null, null)).done(function(data) {
			if (data['result'] == 'success') {
				realtime_words_list = data['search_realtime'].splice(0, 5).reverse();
				for (i = 1; i <= realtime_words_list.length; i++) {
					let word;
					if (realtime_words_list[i - 1] != undefined){
						word = realtime_words_list[i - 1][0];
						div = 	`
									<div class="search_result noselect" onmousedown="search_result_click($(this))">
										<img src="/static/icons/search.png" class="search_result_icon">
										<span class="text_overflow_none">${word}</span>
									</div>
								`;
						target.prepend(div);
					}
				}
			}
		})
	}
	target.append(`<div class="search_loading pointer noselect">
						<i class="fas fa-grip-lines"></i>
					</div>`);
}

// 추천검색어 API
function Insert_recommendation_searchword() {
	// nothing
}

// 메인 페이지 소개 메세지 버튼
let Message_animating = false;
function Main_Info_Message_Btn() {
	if (Message_animating) return;
	let tag = $("#main_info_message_btn");
	let target = $("#main_info_message_area");
	if (target.hasClass("display_none")) {
		tag.attr("src", "/static/icons/message_green.png");
		Message_animating = !Message_animating;
		tag.addClass("main_info_message_btn_selected");
		$.when(A_JAX(host_ip+"/get_main_info", "GET", null, null))
		.done((data) => {
			target.removeClass("display_none");
			messages = data['main_info'];
			new Promise((resolve, reject) => {
				for (let i in messages) {
					let div = `<div class="main_info_message_box pointer wow animated fadeInLeft" onclick="Drop_Main_Info_Message_Btn(this)">${messages[i]}</div>`;
					setTimeout(function(i) {
						target.append(div);
					}, 500*i);
				}
				resolve();
			}).then(() => {
				Message_animating = !Message_animating;
			});
		}).catch((data) => {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		});
	} else {
		tag.attr("src", "/static/icons/message_black.png");
		Message_animating = !Message_animating;
		tag.removeClass("main_info_message_btn_selected");
		$(".main_info_message_box").removeClass("fadeInLeft");
		$(".main_info_message_box").css("animation-name", "fadeOutLeft");
		setTimeout(function() {
			target.empty();
			target.addClass("display_none");
			Message_animating = !Message_animating;
		}, 1000);
	}
}
if (!mobilecheck()) Main_Info_Message_Btn();

function Drop_Main_Info_Message_Btn(tag) {
	$(tag).removeClass("fadeInLeft");
	$(tag).css("animation-name", "fadeOutLeft");
	setTimeout(function() {
		$(tag).remove();
		Check_Main_Info_Message();
	}, 1000);
}

function Check_Main_Info_Message() {
	if ($(".main_info_message_box").length == 0) {
		let tag = $("#main_info_message_btn");
		tag.attr("src", "/static/icons/message_black.png");
		tag.removeClass("main_info_message_btn_selected");
		$("#main_info_message_area").addClass("display_none");
	}
}