// Mobile Device Checked
// mobilecheck()
window.mobilecheck = function() {
	var isMobile = false;
	if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))
	    || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {	// IOS13 UPDATE 
	    isMobile = true;
	}
    return isMobile;
};
// now state
let now_state = "";
// Greetings Array
const greetings = ["반갑습니다!", "환영합니다!", "좋은 하루입니다."];
// Error Imoticon
const imoticons = ["ᵒ̌ ᴥ ᵒ̌ ", "(。・_・。)", "˚ᆺ˚", "( ˃̣̣̥᷄⌓˂̣̣̥᷅ )"];

// Loading Modal
let is_loading = 1;
window.onkeydown = function(e) { 
  if (is_loading == 1)
 	return !(e.keyCode == 32);
};
window.setTimeout(function() {
	is_loading = 0;
}, 1000);



function Goboard() {
	window.location.href = "/board";
}
// 초기 setting
$(document).ready( function() {
	auto_login();
	setTimeout(function() {scroll(0,0);}, 500);
});

// Grid modal on off function
let grid_open = 0;
function grid_modal_onoff() {
	if (mobilecheck()) {
		if (menu_open == 1) menu_modal_onoff();
	}
	if (grid_open == 0) {
		$("#grid").css("background-color", "rgba(0,0,0,.1)");
		$("body").css({"overflow": "hidden"});
		$("#grid_modal").addClass("fadeInUp animated");
		$("#grid_modal").removeClass("display_none");
		setTimeout(function() {
			$("#grid_modal").removeClass("fadeInUp animated");
		}, 400);
		grid_open = 1;
	} else {
		$("#grid").removeAttr("style");
		$("body").removeAttr("style");
		$("#grid_modal").addClass("fadeOutDown");
		$("#mobile_modal_close").addClass("display_none");
		setTimeout(function() {
			$("#grid_modal").removeClass("fadeOutDown animated");
			$("#grid_modal").addClass("display_none");
		}, 400);
		grid_open = 0;
	}
}
function grid_modal_off() {
	if (mobilecheck()) {
		$("#grid").removeAttr("style");
		$("body").removeAttr("style");
		$("#grid_modal").addClass("fadeOutDown");
		setTimeout(function() {
			$("#grid_modal").removeClass("fadeOutDown animated");
			$("#grid_modal").addClass("display_none");
		}, 400);
		$("#mobile_modal_close").addClass("display_none");
		grid_open = 0;
	}
}


// Menu modal on off function
var menu_open = 0;
function menu_modal_onoff(is_menu_open = menu_open) {
	menu_open = is_menu_open;
	if (menu_open == 2) {
		menu_open = 0;
		return;
	}
	if (mobilecheck()) {
		if (grid_open == 1) grid_modal_onoff();
	}
	if (menu_open == 0) {
		$("body").css({"overflow": "hidden"});
		$("#menu_modal").addClass("fadeInUp animated");
		$("#menu_modal").removeClass("display_none");
		setTimeout(function() {
			$("#menu_modal").removeClass("fadeInUp animated");
		}, 400);
		menu_open = 1;
	} else {
		$("body").removeAttr("style");
		$("#menu_modal").addClass("fadeOutDown");
		setTimeout(function() {
			$("#menu_modal").removeClass("fadeOutDown animated");
			$("#menu_modal").addClass("display_none");
		}, 400);
		menu_open = 0;
	}
}
function menu_modal_off() {
	if (mobilecheck()) {
		$("body").removeAttr("style");
		$("#menu_modal").addClass("fadeOutDown");
		setTimeout(function() {
			$("#menu_modal").removeClass("fadeOutDown animated");
			$("#menu_modal").addClass("display_none");
		}, 400);
		menu_open = 0;
	}
}
// 모바일에서 현재 카테고리 클릭하면 메뉴 열리는 함수
function Mobile_menu_modal_onoff() {
	if (!mobilecheck()) return;
	if ($("#board_info_board").text() != "SOOJLE 엔진") {
		menu_modal_onoff();
	} else if ($("#board_info_text").text() == "검색 결과입니다!") {
		menu_modal_onoff();
	} else {
		before_posts();
	}
}


// Login modal on off function
let login_open = 0;
function login_modal_onoff(callback) {
	// 로그인폼 비우기
	$("#user_id").val("");
	$("#user_pw").val("");
	// 회원가입폼 비우기
	$("#signup_id").val("");
	$("#signup_nickname").val("");
	$("#signup_pw").val("");
	$("#signup_pw_check").val("");
	let formInputs = $('#user_id,#user_pw,#signup_id,#signup_nickname,#signup_pw,#signup_pw_check');
	formInputs.focusout();
	if (login_open == 0) {
		$("body").css({"overflow": "hidden"});
		$("#login_modal").removeClass("display_none");
		$("#login_modal").addClass("fadeInUp animated");
		setTimeout(function() {
			$("#login_modal").removeClass("fadeInUp animated");
		}, 400);
		login_open = 1;
	} else {
		$("body").removeAttr("style");
		$("#login_modal").addClass("fadeOutDown");
		setTimeout(function() {
			$("#login_modal").removeClass("fadeOutDown animated");
			$("#login_modal").addClass("display_none");
		}, 400);
		login_open = 0;
	}
	if(typeof callback === 'function') {	// Callback함수 실행
        callback();
    }
}
function open_login_or_setting() {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') {
		Login_open();
	} else {
		menu_open = 1;
		location.replace("/board#setting");
		Go_setting();
	}
}

// Frist Auto Login function
async function auto_login() {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') {
		sessionStorage.removeItem('sj-state');
		token = localStorage.getItem('sj-state');
		if (token == null || token == undefined || token == 'undefined') {
			localStorage.removeItem('sj-state');
			if (window.location.href.search("#search?") != -1) {
				// 로딩 모달 제거
				$("#mobile_controller_none").addClass("display_none");
				$("#board_loading_modal").addClass("board_loading_modal_unvisible");
				$(".mobile_controller").removeAttr("style");
				$("#none_click").addClass("display_none");
				let text = decodeURI(window.location.href);
				text = text.split("#search?")[1];
				text = text.split("/")[0];
				text = text.replace(/\+/g, " ");
				$("#board_logo").css({"left": "10px",
								"transform": "translate(0, 0)",
								"-webkit-transform": "translate(0, 0)"});
				$("#mobile_search").removeClass("display_none");
				//search_open = 1;
				$("#mobile_search_recommend_box").removeClass("display_none");
				await search_text(text);
			} else if (window.location.href.search("#") != -1) {
				await URL_Detection();
			} else { // 메인에서 검색을 하지않았다면 추천 뉴스피드 호출
				get_recommend_posts(1);
			}
			return;
		} else {
			sessionStorage.setItem('sj-state', localStorage.getItem('sj-state'));
		}
	}
	Get_UserInfo(function(result) {
		if (result) {
			if (result['result'] == 'success') {
				After_login(result);
				Menu_User_Info_Change(result['user_nickname']);	// 좌측 메뉴 닉네임 변경
			} else {
				Menu_User_Info_Change("사용자");	// 좌측 메뉴 닉네임 변경
				Snackbar("서버와의 연결이 원활하지 않습니다.");
			}
		}
	});
}


// 로그인 후, 사용자 정보 수정
function Menu_User_Info_Change(nickname) {
	let hello = greetings[Math.floor(Math.random() * greetings.length)];
	nickname = nickname + "님, " + hello;
	$("#user_info").text(nickname);
	$("#user_info_mobile").text(nickname);
}
async function After_login() {
	Snackbar("맞춤 서비스를 시작합니다.");
	check_manager_qualification();
	$("#sign_up_button").addClass("display_none");
	$("#login_button").addClass("display_none");
	$("#view_button").removeClass("display_none");
	$("#like_button").removeClass("display_none");
	$("#logout_button").removeClass("display_none");
	if (mobilecheck()) {
		$("#user_login_mobile").addClass("display_none");
		$("#user_info_mobile").removeClass("display_none");
	} else {
		$("#user_login").addClass("display_none");
		$("#user_info").removeClass("display_none");
	}
	// 메인에서 검색을 했다면 검색 결과 호출
	if (window.location.href.search("#search?") != -1) {
		// 로딩 모달 제거
		$("#mobile_controller_none").addClass("display_none");
		$("#board_loading_modal").addClass("board_loading_modal_unvisible");
		$(".mobile_controller").removeAttr("style");
		$("#none_click").addClass("display_none");
		let text = decodeURI(window.location.href);
		text = text.split("#search?")[1];
		text = text.replace(/\+/g, " ");
		$("#board_logo").css({"left": "10px",
								"transform": "translate(0, 0)",
								"-webkit-transform": "translate(0, 0)"});
		$("#mobile_search").removeClass("display_none");
		search_open = 1;
		$("#mobile_search_recommend_box").removeClass("display_none");
		text = text.split("/")[0];
		text = text.replace(/\+/g, " ");
		await search_text(text);
	} else if (window.location.href.search("#") != -1) {
		await URL_Detection();
	} else {
		location.replace("/board#recommend");
	}
}

// button click ripple event
$("html").on("click", ".ripple", function(evt) {
	let ripple = $(evt.currentTarget);
	let x = evt.pageX - ripple.offset().left;
	let y = evt.pageY - ripple.offset().top;
	let duration = 1000;
	let animationFrame, animationStart;
	let animationStep = function(timestamp) {
		if (!animationStart) {
			animationStart = timestamp;
		}
		let frame = timestamp - animationStart;
		if (frame < duration) {
			let easing = (frame/duration) * (2 - (frame/duration));
			let circle = "circle at " + x + "px " + y + "px";
			let color = "rgba(0, 0, 0, " + (0.3 * (1 - easing)) + ")";
			let stop = 90 * easing + "%";
			ripple.css({
				"background-image": "radial-gradient(" + circle + ", " + color + " " + stop + ", transparent " + stop + ")"
			});
			animationFrame = window.requestAnimationFrame(animationStep);
		} else {
			$(ripple).css({
				"background-image": "none"
			});
			window.cancelAnimationFrame(animationFrame);
		}
	};
	animationFrame = window.requestAnimationFrame(animationStep);
});


function Go_home() {
	window.location.href = "/";
}

function Login() {
	menu_modal_onoff();
	SignUp_open();
}
function Logout() {
	localStorage.removeItem("sj-state");
	sessionStorage.removeItem("sj-state");
	location.replace("/board");
}
function pageUp() {
	scroll(0,0);
	$("#pc_search_input").focus();
}


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
		$.when(A_JAX(host_ip+"/get_search_realtime", "GET", null, null))
		.done(function(data) {
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
	target.append(`<div class="search_loading pointer noselect" onclick="search_blur()">
						<i class="fas fa-grip-lines"></i>
					</div>`);
}