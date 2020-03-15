const ABORT_ID = ['admin', '관리자', 'soojle', '수즐'];	// 불가능한 ID 및 닉네임
let agreement_open = 0;

// 개인정보처리방침 동의===========================================================
// 모달 On/Off
function agreement() {
	if (agreement_open == 0) {
		agreement_open = !agreement_open;
		$("body").css({"overflow": "hidden"});
		$("#user_agreement_modal").removeClass("display_none");
		$("#user_agreement_modal").addClass("fadeInUp animated");
		$("#license_block").append(privacy_1);
	} else {
		agreement_open = !agreement_open;
		$("#user_agreement_modal").addClass("fadeOutDown");
		setTimeout(function() {
			$("#user_agreement_modal").removeClass("fadeOutDown animated");
			$("#user_agreement_modal").addClass("display_none");
			$("#license_block").empty();
		}, 400);
	}
}
// 버튼 Event
$("#privacy_ok_btn").on({
	"click": function() {
		agreement();	// 개인정보처리방침 동의모달 닫기
		Sign_Up_Send();
	}
});
$("#privacy_no_btn").on({
	"click": function() {
		agreement();	// 개인정보처리방침 동의모달 닫기
	}
});

// 입력 폼 Animation==============================================================
$(document).ready(function(){
	let formInputs = $('#user_id,#user_pw,#signup_id,#signup_nickname,#signup_pw,#signup_pw_check');
	formInputs.focus(function() {
       $(this).parent().children('p.formLabel').addClass('formTop');
	});
	formInputs.focusout(function() {
		if ($.trim($(this).val()).length == 0){
			$(this).parent().children('p.formLabel').removeClass('formTop');
		}
	});
	$('p.formLabel').click(function(){
		 $(this).parent().children('.login_input').focus();
	});
});

// 로그인/회원가입 선택=============================================================
$("#select_login_form").on({	// 로그인 폼 선택 
	"click": function() {
		$("#select_signup_form").removeClass("login_title_select");
		$("#select_login_form").addClass("login_title_select");
		$("#LoginTab").removeClass("display_none");
		$("#SignUpTab").addClass("display_none");
		$("#user_id").focus();
	}
});
$("#select_signup_form").on({	// 회원가입 폼 선택
	"click": function() {
		$("#select_login_form").removeClass("login_title_select");
		$("#select_signup_form").addClass("login_title_select");
		$("#SignUpTab").removeClass("display_none");
		$("#LoginTab").addClass("display_none");
		$("#signup_id").focus();
	}
});
function Login_open() {
	$("#LoginTab").removeClass("display_none");
	$("#SignUpTab").addClass("display_none");
	$("#select_login_form").addClass("login_title_select");
	$("#select_signup_form").removeClass("login_title_select");
	login_modal_onoff(function() {
		setTimeout(function() {$("#user_id").focus();}, 100);
	});
}
function SignUp_open() {
	$("#LoginTab").addClass("display_none");
	$("#SignUpTab").removeClass("display_none");
	$("#select_login_form").removeClass("login_title_select");
	$("#select_signup_form").addClass("login_title_select");
	login_modal_onoff(function() {
		$("#signup_id").focus();
	});
}


// 로그인==========================================================================
function Sign_in_check() {								// 로그인란 공백 검사
	if ($("#user_id").val() == "") {
		Snackbar("학번 또는 교번을 입력해주세요.");
		$("#user_id").focus();
		return false;
	} else if ($("#user_pw").val() == "") {
		Snackbar("비밀번호를 입력해주세요.");
		$("#user_pw").focus();
		return false;
	}
	return true;						// 로그인란 공백 검사
}
function Sign_in() {									// 로그인 완료 버튼
	if (Sign_in_check()) {
		let user_id = $("#user_id").val();
		let user_pw = $("#user_pw").val();
		let send_data = {id: user_id, pw: user_pw};
		$("#loading_modal").removeClass("loading_modal_unvisible");
		$.when(A_JAX(host_ip+"/sign_in", "POST", null, send_data))
		.done(function (data) {
			$("#loading_modal").addClass("loading_modal_unvisible");
			if (data['result'] == 'success') {
				let token = data['access_token'];
				sessionStorage.setItem('sj-state', token);
				window.location.replace("/board#recommend");
				Get_UserInfo(function(result) {
					nickname = "사용자";
					if (result) {
						nickname = result["user_nickname"];
						login_modal_onoff();
						$("#user_id").val("");
						$("#user_pw").val("");
						if (result['auto_login'] == 1)
							localStorage.setItem("sj-state", sessionStorage.getItem('sj-state'));
						After_login();
					} else {
						Snackbar("서버와의 연결이 원활하지 않습니다.");
						localStorage.removeItem('sj-state');
						sessionStorage.removeItem('sj-state');
					}
					Menu_User_Info_Change(nickname);
				});
			} else if (data['result'] == 'Incorrect pw') {
				Snackbar("비밀번호를 다시 입력해주세요.");
				localStorage.removeItem('sj-state');
				sessionStorage.removeItem('sj-state');
			} else if (data['result'] == 'Not found') {
				Snackbar("존재하지 않는 회원입니다.");
				sessionStorage.removeItem('sj-state');
				localStorage.removeItem('sj-state');
			} else {
				Snackbar("잠시 후 다시 시도해주세요.");
			}
		}).catch((data) => {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		});
	}
	return false;
}
function SignIn_id_Check(tag) {							// 로그인 ID 검사
	// ID 길이는 6~30자 사이
	if ($(tag).val().length >= 6
	 && $(tag).val().length <= 30
	 && ABORT_ID.indexOf($(tag).val().toLowerCase()) == -1) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
	}
	return false;
}
function SignIn_pw_Check(tag) {							// 로그인 PW 검사
	if ($(tag).val().length >= 8) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
	}
	return false;
}
function Enter_login(event) {								// 로그인 키 입력
	SignIn_id_Check($("#user_id"));
	SignIn_pw_Check($("#user_pw"));
	CapsLock_Check(event);									// CapsLock 검사
	// Enter 누를 시
	if (event.keyCode == 13) {
        if ($("#user_id").val() == "") {
        	Snackbar("아이디를 입력해주세요.");
        	$("#user_id").focus();
        } else if ($("#user_pw").val() == "") {
        	Snackbar("비밀번호를 다시 입력해주세요.");
        	$("#user_pw").focus();
        } else {
        	Sign_in();
        }
    }
}
function CapsLock_Check(event) {						// CapsLock 검사
	let key = event.key, shiftKey = event.shiftKey;
	if (key == undefined) return;
	if (((key.match(/^[A-Z]$/)) && !shiftKey)
	 || ((key.match(/^[a-z]$/)) && shiftKey)) {
	 	if (event.target.id == "user_pw")
			Snackbar("CapsLock이 켜져있습니다.");			// 임시 코드
	}
}
$("#user_id, #user_pw").keydown(function(event) {
	Enter_login(event);
});

// 회원가입=========================================================================
function SignUp_blank_Check() {					// 회원가입란 공백 검사
	if ($("#signup_id").val() == '') {
		Snackbar("아이디를 입력해주세요.");
		$("#signup_id").focus();
		return false;
	} else if ($("#signup_nickname").val() == '') {
		Snackbar("닉네임을 입력해주세요.");
		$("#signup_nickname").focus();
		return false;
	} else if ($("#signup_pw").val() == '') {
		Snackbar("비밀번호를 입력해주세요.");
		$("#signup_pw").focus();
		return false;
	} else if ($("#signup_pw_check").val() == '') {
		Snackbar("비밀번호를 다시 입력해주세요.");
		$("#signup_pw_check").focus();
		return false;
	}
	return true;
}
function SignUp_id_Check(tag) {					// 회원가입 ID 검사
	// ID 길이는 6~30자 사이
	if ($(tag).val().length == 0) {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
	} else if ($(tag).val().length >= 6
	 && $(tag).val().length <= 30
	 && ABORT_ID.indexOf($(tag).val().toLowerCase()) == -1) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-check-circle signup_check_img_ok"></i>`);
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-exclamation-triangle signup_check_img_warning"></i>`);
	}
	return false;
}
function SignUp_nickname_Check(tag) {			// 회원가입 닉네임 검사
	if ($(tag).val().length == 0) {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
	} else if ($(tag).val().length >= 1
	 && $(tag).val().length <= 16
	 && ABORT_ID.indexOf($(tag).val().toLowerCase()) == -1) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-check-circle signup_check_img_ok"></i>`);
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-exclamation-triangle signup_check_img_warning"></i>`);
	}
	return false;
}
function Change_nickname_Check(str) {			// 닉네임 공백란 검사
	if (str.length >= 1 && str.length <= 16 && ABORT_ID.indexOf(str.toLowerCase()) == -1)
		return true;
	return false;
}
function SignUp_pw_Check(tag) {					// 회원가입 PW 검사
	let check_num = 0;
	if ($(tag).val().length == 0) {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
		$("#pwleast").removeAttr("style");
		$("#pwletternum").removeAttr("style");
		$("#pwsymbol").removeAttr("style");
		return false;
	}
	// 공백 포함 확인
	if($(tag).val().search(/\s/) != -1) {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		return false;
	}
	// 최소 8자리 확인
	if ($(tag).val().length >= 8) {
		check_num += 1;
		$("#pwleast").css("color", "#12b886");
	} else {
		$("#pwleast").removeAttr("style");
	}
	// 문자와 숫자포함 확인
	let pw_guideline = /(?=.*\d)(?=.*[a-z])/;
	if (pw_guideline.test($(tag).val().toLowerCase())) {
		check_num += 1;
		$("#pwletternum").css("color", "#12b886");
	} else {
		$("#pwletternum").removeAttr("style");
	}
	// 특수기호 포함 확인
	pw_guideline = /[`~!@#$%^&*|\\\'\";:\/?]/gi;
	if (pw_guideline.test($(tag).val().toLowerCase())) {
		check_num += 1;
		$("#pwsymbol").css("color", "#12b886");
	} else {
		$("#pwsymbol").removeAttr("style");
	}
	// 모든 조건 포함
	if (check_num == 3) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-check-circle signup_check_img_ok"></i>`);
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-exclamation-triangle signup_check_img_warning"></i>`);
	}
	return false;
}
function SignUp_pw_same_Check(pw_tag, tag) {	// 회원가입 PW 재확인 검사
	let pw_before = $(pw_tag).val();
	if ($(tag).val().length == 0) {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
	} else if ($(tag).val() === pw_before) {
		$(tag).css("border", "2px solid #12b886");
		$($(tag).next()[0]).css("color", "#12b886");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-check-circle signup_check_img_ok"></i>`);
		return true;
	} else {
		$(tag).removeAttr("style");
		$($(tag).next()[0]).removeAttr("style");
		$($(tag).siblings(":last")[0]).empty();
		$($(tag).siblings(":last")[0]).append(`<i class="fas fa-exclamation-triangle signup_check_img_warning"></i>`);
	}
	return false;
}

function Key_Signup() {		// 회원가입 키 입력
	if (window.event.keyCode == 13) {
		if (SignUp_blank_Check()) Sign_Up();
	} else {
		let now_tag = window.event.target;
		if (now_tag.id == "signup_id") {
			SignUp_id_Check(now_tag);
		} else if (now_tag.id == "signup_nickname") {
			SignUp_nickname_Check(now_tag);
		} else if (now_tag.id == "signup_pw") {
			SignUp_pw_Check(now_tag);
			if (window.event.getModifierState("CapsLock")) {	// CapsLock
				CapsLock_Check($(now_tag));
			}
		} else if (now_tag.id == "signup_pw_check") {
			SignUp_pw_same_Check(document.querySelector('#signup_pw'), now_tag);
			if (window.event.getModifierState("CapsLock")) {	// CapsLock
				CapsLock_Check($(now_tag));
			}
		}
	}
}
function Sign_Up() {		// 회원가입 완료 버튼
	if (!SignUp_blank_Check()) return;	// 빈 칸 확인
	if (!SignUp_id_Check(document.querySelector('#signup_id'))) {
		Snackbar("아이디를 다시 입력해주세요.");
		$("#signup_id").select().focus();
		return;
	}
	if (!SignUp_nickname_Check(document.querySelector('#signup_nickname'))) {
		Snackbar("닉네임을 다시 입력해주세요.");
		$("#signup_nickname").select().focus();
		return;
	}
	if (!SignUp_pw_Check(document.querySelector('#signup_pw'))) {
		Snackbar("비밀번호를 다시 입력해주세요.");
		$("#signup_pw").select().focus();
		return;
	}
	if (!SignUp_pw_same_Check(document.querySelector('#signup_pw'), document.querySelector('#signup_pw_check'))) {
		Snackbar("동일한 비밀번호를 입력해주세요.");
		$("#signup_pw_check").select().focus();
		return;
	}
	agreement();
}
function Sign_Up_Send() {	// 회원가입 API 호출
	let sendData = {};
	sendData['id'] = $("#signup_id").val();
	sendData['nickname'] = $("#signup_nickname").val();
	sendData['pw'] = $("#signup_pw").val();
	sendData['pw_check'] = $("#signup_pw_check").val();
	$.when(A_JAX(host_ip+"/sign_up", "POST", null, sendData)).done(function (data) {
		if (data['result'] == 'success') {
			let token = data['access_token'];
			sessionStorage.setItem('sj-state', token);
			localStorage.setItem('sj-state', token);
			window.location.replace("/board#recommend");
			location.reload();
		} else if (data['result'] == 'Exist') {
			Snackbar("이미 존재하는 아이디입니다.");
			$("#signup_id").select().focus();
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
	}).catch((data) => {
		if (data['status'] == 400) {
			Snackbar("잘못된 요청입니다.");
			$("#signup_pw_check").select().focus();
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		}
	});
}
// 회원가입란 Event Binding
$("#signup_id,#signup_nickname,#signup_pw,#signup_pw_check").keyup(function() {
	Key_Signup();
});



// 회원정보=========================================================================
// ID 찾기
function Find_ID() {
	login_modal_onoff();	// Off Login Modal
}
// PW 찾기
function Find_PW() {
	login_modal_onoff();	// Off Login Modal
}
// 회원정보 반환 (callback(<userdata>))
function Get_UserInfo(callback) {
	let token = sessionStorage.getItem('sj-state');
    if (token == null || token == undefined || token == 'undefined') {
    	sessionStorage.removeItem('sj-state');
    	return false;
    }
    let output = {};
	$.when(A_JAX(host_ip+"/get_userinfo", "GET", null, null)).done(function (data) {
		if (data['result'] == 'success') {
			if (typeof(callback) == 'function') {
				callback(data);
			}
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
			return false;
		}
	}).catch((data) => {
		if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
			window.location.reload();
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
	return output;
}
// 관리자 확인 반환 (callback(<userdata>))
function Check_ManagerInfo(callback) {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') return;
	Get_UserInfo((result) => {
		if (result["admin"] == 1) {
			if (typeof(callback) == "function") {
				callback();
			}
		}
	});
}
// 최근 본 게시글 반환 (callback(<userdata>))
function Get_Recently_View_Post(callback) {
	$.when(A_JAX(host_ip+"/get_specific_userinfo/"+2, "GET", null, null))
	.done(function (data) {
		let output = [];
		if (data['result'] == 'success') {
			output = JSON.parse(data["user"]);
			output = output['view_list'];
			if (typeof(callback) == 'function') {
				callback(output);
			}
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
		return output;
	}).catch((data) => {
		if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
			window.location.reload();
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
}
// 좋아요 게시글 반환 (callback(<userdata>))
function Get_Like_Post(callback) {
	$.when(A_JAX(host_ip+"/get_specific_userinfo/"+1, "GET", null, null))
	.done(function (data) {
		let output = [];
		if (data['result'] == 'success') {
			output = JSON.parse(data["user"]);
			output = output['fav_list'];
			if (typeof(callback) == 'function') {
				callback(output);
			}
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
		return output;
	}).catch((data) => {
		if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
			window.location.reload();
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
}

// 사용자 최근 검색어 반환
function Get_recently_searchword(callback) {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') {
		if (typeof(callback) == 'function') {
			callback([]);
		}
		return;
	};
	$.when(A_JAX(host_ip+"/get_user_lately_search/"+10, "GET", null, null))
	.done(function(data) {
		if (data['result'] == "success") {
			if (typeof(callback) == 'function') {
				callback(data["lately_search_list"]);
			}
		}
	}).catch((data) => {
		if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
			window.location.reload();
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
}