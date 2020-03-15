function Go_feedback() {
	location.href = "/board#feedback";
	out_of_search();
	now_topic = "Feedback";
	where_topic = "Feedback";
	now_state = "Feedback";
	$("#board_info_board").text("SOOJLE");
	$("#board_info_text").text("피드백 보내기");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);
	menu_modal_onoff();
	insert_feedback_div();
}

function insert_feedback_div() {
	let feedback_placeholder = 
`내용을 입력해주세요.

반드시 위 구분을 선택하여 작성해주세요.
버그 및 오류 피드백일 경우에는 상세하게 작성해주시면 감사합니다.

※입력예시
- 검색에서 버그가 발생했어요! (X)
- 검색과정에서 탭을 연속적으로 클릭하면 게시글이 삭제되요! (O)
`;
	let div =	`<div class="setting_subject_wrap">
					<div class="setting_title noselect">사용자 피드백</div>
					<div class="setting_title_info noselect">
						수즐에게 사용자 의견을 공유할 수 있습니다.
					</div>
				</div>
				<div class="selectbox_container">
					<div class="selectbox_dropdown">
						<div class="selectbox_select">
							<span>구분</span>
							<i class="fa fa-chevron-left"></i>
						</div>
						<input type="hidden" name="gender">
						<ul class="selectbox_dropdown-menu">
							<li id="feedback_pc_bug">데스크탑 버그 및 오류</li>
							<li id="feedback_mobile_bug">모바일/태블릿 버그 및 오류</li>
							<li id="feedback_hack">취약점 및 보안 개선</li>
							<li id="feedback_design">디자인 개선 아이디어</li>
							<li id="feedback_function">기능 개선 아이디어</li>
							<li id="feedback_function">기타</li>
						</ul>
					</div>
				</div>
				<textarea id="feedback_box" class="feedback_box" placeholder="${feedback_placeholder}"></textarea>
				<div class="feedback_send_btn pointer" onclick="feedback_send();">전송하기</div>
				`;
	$("#posts_target").append(div);
	$("#posts_creating_loading").addClass("display_none");
	selectbox_action();
}
let selectbox_input = "구분";
// Select Box JS
function selectbox_action() {
	/*Dropdown Menu*/
	$('.selectbox_dropdown').click(function () {
	        $(this).attr('tabindex', 1).focus();
	        $(this).toggleClass('selectbox_active');
	        $(this).find('.selectbox_dropdown-menu').slideToggle(300);
	    });
	    $('.selectbox_dropdown').focusout(function () {
	        $(this).removeClass('selectbox_active');
	        $(this).find('.selectbox_dropdown-menu').slideUp(300);
	    });
	    $('.selectbox_dropdown .selectbox_dropdown-menu li').click(function () {
	        $(this).parents('.selectbox_dropdown').find('span').text($(this).text());
	        $(this).parents('.selectbox_dropdown').find('input').attr('value', $(this).attr('id'));
	    });
	/*End Dropdown Menu*/
	$('.selectbox_dropdown-menu li').click(function () {
		selectbox_input = $(this).attr("id");
		if (selectbox_input == "feedback_pc_bug") selectbox_input = "데스크탑 버그 및 오류";
		else if (selectbox_input == "feedback_mobile_bug") selectbox_input= "모바일/태블릿 버그 및 오류";
		else if (selectbox_input == "feedback_hack") selectbox_input = "취약점 및 보안 개선";
		else if (selectbox_input == "feedback_design") selectbox_input = "디자인 개선 아이디어";
		else if (selectbox_input == "feedback_function") selectbox_input = "기능 개선 아이디어";
		else if (selectbox_input == "feedback_function") selectbox_input = "기타";
		else selectbox_input = "Abnormal approach:404";
	});
}

function feedback_send() {
	if (selectbox_input == "구분") {
		Snackbar("피드백 구분을 선택해주세요.");
		return;
	}
	let send_data = {};
	let phragh = $("#feedback_box").val();
	if (phragh == "") {
		Snackbar("내용을 입력해주세요.");
		$("#feedback_box").focus();
		return;
	} else if (phragh.length > 1000) {
		Snackbar("제한 길이를 초과하였습니다.");
		$("#feedback_box").focus();
		return;
	}
	send_data["type"] = selectbox_input;
	send_data["post"] = phragh;
	
	$.when(A_JAX(host_ip+"/send_feedback", "POST", null, send_data))
	.done(function (data) {
		if (data['result'] = 'success') {
			Snackbar("피드백을 전송하였습니다.");
			$("#feedback_box").val("");
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
	}).catch((data) => {
		if (data.status == 400) {
			Snackbar("잘못된 요청입니다.");
		} else if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		}
	});
}