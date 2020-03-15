function Click_setting() {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') {
		if (menu_open == 1) menu_modal_onoff();
		Snackbar("로그인이 필요합니다.");
		Login_open();
		return;
	}
	location.href = "/board#setting";
	if (menu_open == 1) {
		menu_modal_onoff();
	}
}

// Setting Page 구성 함수
function Go_setting() {
	out_of_search();
	$('body,html').animate({ scrollTop: 0, }, 0);
	$("#menu_container").removeClass("menu_container_fixed");
	$("#posts_creating_loading").addClass("display_none");
	let token = sessionStorage.getItem('sj-state');
	$("#posts_target").empty();
	$("#posts_target").append(`<div id="setting_box" class="setting_box"></div>`)
	$("#board_info_text").text("설정");
	$("#board_info_board").text("SOOJLE");
	insert_user_custom_setting();
	insert_user_information_setting();
	now_topic = "설정";
	where_topic = "SOOJLE";
	now_state = now_topic;
	if (token == null || token == undefined || token == 'undefined') {
		Snackbar("로그인이 필요합니다.");
		Login_open();
	} else {
		Get_UserInfo(function(result) {	// result == 유저정보
			if (result) {
				// 자동로그인 Option Setting
				if (result['auto_login'] == 1) {
					$("#autologin_toggle").prop("checked", true);
				} else {
					localStorage.removeItem('sj-state');
					$("#autologin_toggle").prop("checked", false);
				}
				// 닉네임 Setting
				Set_nickname(result['user_nickname']+'');
			}
		})
	}
	menu_modal_onoff();
}

// 사용자 맞춤 설정 Insert
function insert_user_custom_setting() {
	let token = sessionStorage.getItem('sj-state');
	// Title & Subtitle
	let title_info_1 = "각 사용자에게 맞는 SOOJLE 서비스 환경설정";
	let st_1 = "자동로그인"
	let st_info_1 = "로그인을 자동화해 SOOJLE 서비스 이용을 간편하게 합니다.";
	// Tag================================================================
	// 자동로그인 옵션
	let autologin_div = ``;	
	if (token != null && token != undefined && token != 'undefined' && token != 'null') {
		autologin_div = `
						<div>
							<div class="setting_subtitle noselect">${st_1}</div>
							<input type="checkbox" id="autologin_toggle" onchange="change_autologin_st()" name="autologin_toggle">
							<div class="setting_toggle">
								<label for="autologin_toggle"></label>
							</div>
							<div class="setting_subtitle_info noselect">${st_info_1}</div>
						</div>
						`;
	}
	let div =	`
					<div class="setting_subject_wrap">
						<div class="setting_title noselect">사용자 맞춤</div>
						<div class="setting_title_info noselect">${title_info_1}</div>
						${autologin_div}
					</div>
					
				`;
	$("#setting_box").append(div);
}
// 사용자 개인정보 설정 Insert
function insert_user_information_setting() {
	let token = sessionStorage.getItem('sj-state');
	// Title & Subtitle
	let title_info_1 = "사용자 계정에 대한 정보 관리 및 설정";
	let st_1 = "계정삭제";
	let st_info_1 = "사용자의 정보를 SOOJLE 데이터베이스에서 완전 삭제합니다.";
	let st_2 = "관심도 초기화";
	let st_info_2 = "사용자의 모든 기록을 삭제하여, 사용자 관심도를 초기화합니다.";
	let st_3 = "닉네임 변경";
	let st_info_3 = "사용자의 닉네임을 변경합니다.";

	// 로그인이 되어있지 않으면 return
	if (token == null || token == undefined || token == 'undefined' || token == 'null') return;
	// Tag================================================================
	let user_information_div = `
								<div class="setting_subject_wrap">
									<div class="setting_title noselect">개인정보 설정</div>
									<div class="setting_title_info noselect">${title_info_1}</div>

									<div>
										<div class="setting_subtitle noselect">${st_3}</div>
										<div id="setting_nickname_cancel" class="setting_edit_cancel display_none" onclick="Cancel_nickname()"><i class="fas fa-times"></i></div>
										<div id="setting_nickname_check" class="setting_edit_check display_none" onclick="Change_nickname()"><i class="fas fa-check"></i></div>
										<div id="setting_nickname_edit" class="setting_edit" onclick="Edit_nickname()"><i class="fas fa-pen-fancy"></i></div>
										<div class="setting_subtitle_info noselect">${st_info_3}</div>
										<div class="setting_nickname_container">
											<div id="setting_nickname_guideline" class="setting_nickname_guideline noselect"></div>
											<input type="text" id="setting_nickname_edit_guideline" class="setting_nickname_guideline_input display_none">
										</div>
									</div>

									<div>
										<div class="setting_subtitle noselect" style="color:#c30e2e">${st_2}</div>
										<div id="user_data_reset" class="setting_btn" onclick="change_userreset_st()">초기화</div>
										<div class="setting_subtitle_info noselect">${st_info_2}</div>
									</div>
									
									<div>
										<div class="setting_subtitle noselect" style="color:#c30e2e">${st_1}</div>
										<div id="user_data_delete" class="setting_btn" onclick="change_userdelete_st()">삭제</div>
										<div class="setting_subtitle_info noselect">${st_info_1}</div>
									</div>
								</div>
								`

	let div = 	`
					${user_information_div}
				`;
	$("#setting_box").append(div);
	// 닉네임 Input Event Binding
	Keyup_nickname();
}



// 사용자 맞춤 설정 관련===================================================================

// 자동로그인 옵션화
function change_autologin_st(){
	if($("#autologin_toggle").is(":checked")) {
		localStorage.setItem("sj-state", sessionStorage.getItem('sj-state'));
		$.when(A_JAX(host_ip+"/update_auto_login/" + 1, "GET", null, null))
		.done((data) => {})
		.catch((data) => {
			if (data.status == 400) {
				Snackbar("잘못된 요청입니다.");
			} else if (data.status == 401) {
				Snackbar("다시 로그인 해주세요.");
			} else {
				Snackbar("서버와의 연결이 원활하지 않습니다.");
			}
		});
	} else {
		localStorage.removeItem('sj-state');
		$.when(A_JAX(host_ip+"/update_auto_login/" + 0, "GET", null, null))
		.done((data) => {})
		.catch((data) => {
			if (data.status == 400) {
				Snackbar("잘못된 요청입니다.");
			} else if (data.status == 401) {
				Snackbar("다시 로그인 해주세요.");
			} else {
				Snackbar("서버와의 연결이 원활하지 않습니다.");
			}
		});
	}
}


// 사용자 개인정보 설정 관련================================================================
// 사용자 닉네임 표시
function Set_nickname(nickname) {
	$("#setting_nickname_guideline").text(nickname);
}
// 사용자 닉네임 변경준비
function Edit_nickname() {
	$("#setting_nickname_edit").addClass("display_none");
	$("#setting_nickname_guideline").addClass("display_none");
	$("#setting_nickname_check").removeClass("display_none");
	$("#setting_nickname_cancel").removeClass("display_none");
	$("#setting_nickname_edit_guideline").removeClass("display_none");
	$("#setting_nickname_edit_guideline").val($("#setting_nickname_guideline").text());
	$("#setting_nickname_edit_guideline").select();
	$("#setting_nickname_edit_guideline").focus();
}
// 사용자 닉네임 변경수신
function Change_nickname() {
	let nickname = $("#setting_nickname_edit_guideline").val();
	if (!Change_nickname_Check(nickname)) {
		Snackbar("잘못된 닉네임입니다.");
		return false;
	}
	let sendData = {};
	sendData['new_nickname'] = nickname;
	$.when(a_jax = A_JAX(host_ip+"/change_nickname", "POST", null, sendData)).done(function (data) {
		if (data['result'] == 'success') {
			$("#setting_nickname_guideline").text(nickname);
			Menu_User_Info_Change(nickname);
			Snackbar("닉네임이 변경되었습니다.");
			Cancel_nickname();
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
	}).catch((data) => {
		if (data['status'] == 400) {
			Snackbar("잘못된 요청입니다.");
		} else if (data['status'] == 401) {
			Snackbar("다시 로그인 해주세요.");
		} else {
			Snackbar("서버와의 통신이 원활하지 않습니다.");
		}
	});
	return true;
}
// 사용자 닉네임 변경취소
function Cancel_nickname() {
	$("#setting_nickname_edit").removeClass("display_none");
	$("#setting_nickname_guideline").removeClass("display_none");
	$("#setting_nickname_check").addClass("display_none");
	$("#setting_nickname_cancel").addClass("display_none");
	$("#setting_nickname_edit_guideline").addClass("display_none");
	$("#setting_nickname_edit_guideline").val("");
}
// 사용자 닉네임 Key Up Binding
function Keyup_nickname() {
	$("#setting_nickname_edit_guideline").keyup(function() {
		if (window.event.keyCode == 13 &&
			$("#setting_nickname_edit_guideline").val() != '') {
			Change_nickname();
		}
	});
}

// 사용자 정보 초기화
function change_userreset_st() {
	$("#user_data_delete_info").empty();
	$("#user_data_delete_info").append(`관심도를 초기화하기 위해서는 "<span style="font-weight: bold">관심도 초기화</span>"를 입력한 다음에 확인을 눌러주세요.`);
	$("#user_data_delete_button_ok").attr("onclick", "user_data_reset_button_ok()");
	$("#user_data_modal_container").removeClass("display_none");
	$("body").css("overflow", "hidden");
	$("#user_data_delete_input").val("");
	$("#user_data_delete_input").focus();
}
function user_data_reset_button_ok() {
	let val = $("#user_data_delete_input").val();
	if (val != "관심도 초기화") {
		Snackbar("입력이 잘못되었습니다.");
		$("#user_data_delete_input").focus();
		return;
	}
	$.when(A_JAX(host_ip+"/reset_user_measurement", "GET", null, null))
	.done((data) => {
		if(data['result'] == 'success') {
			Snackbar("관심도가 초기화 되었습니다.");
			user_data_modal_cancel();
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
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
// 사용자 정보 삭제
function change_userdelete_st() {
	$("#user_data_delete_info").empty();
	$("#user_data_delete_info").append(`계정을 삭제하기 위해서는 "<span style="font-weight: bold">SOOJLE 계정삭제</span>"를 입력한 다음에 확인을 눌러주세요.`);
	$("#user_data_delete_button_ok").attr("onclick", "user_data_delete_button_ok()");
	$("#user_data_modal_container").removeClass("display_none");
	$("body").css("overflow", "hidden");
	$("#user_data_delete_input").val("");
	$("#user_data_delete_input").focus();
}
function user_data_delete_button_ok() {
	let val = $("#user_data_delete_input").val();
	if (val != "SOOJLE 계정삭제") {
		Snackbar("입력이 잘못되었습니다.");
		$("#user_data_delete_input").focus();
		return;
	}
	$.when(A_JAX(host_ip+"/delete_user", "GET", null, null))
	.done((data) => {
		if(data['result'] == 'success') {
			Snackbar("계정이 삭제되었습니다.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
			location.replace("/board#recommend");
			location.reload();
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
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
	});;
}
// 사용자 정보 모달 취소 버튼
function user_data_modal_cancel() {
	$("#user_data_modal_container").addClass("display_none");
	$("body").removeAttr("style");
}
// 사용자 정보 초기화/삭제 키 입력
$("#user_data_delete_input").on({	// 회원가입 폼 선택
	"keyup": function() {
		if (window.event.keyCode == 13) {
			if ($("#user_data_delete_button_cancel").attr("onclick") == 'user_data_reset_button_cancel()') {
				user_data_reset_button_ok();	
			} else {
				user_data_delete_button_ok();
			}
		}
	}
});