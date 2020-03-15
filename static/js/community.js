const NOTICE_PLACEHOLDER = 
`내용을 입력해주세요.

공지사항을 작성 시, 다음 규칙을 확인하고 올려주세요.

[공지사항 작성 유의사항]
1. 욕설, 비하, 음란물, 개인정보가 포함된 게시물 게시.
2. 특정인이나 단체/지역을 비방하는 행위.
3. 기타 현행법에 어긋나는 행위.
`;

// 공지사항 클릭
function Click_dvnote() {
	location.href = "/board#dvnote";
	menu_modal_onoff();
}
// 공지사항으로 이동
function Go_dvnote() {
	let url_target = window.location.href.split("#")[1];
	out_of_search();
	now_topic = "개발자노트";
	where_topic = "개발자노트";
	now_state = "개발자노트";
	$("#board_info_board").text("SOOJLE");
	$("#board_info_text").text("개발자노트");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);
	menu_modal_onoff();
	if (url_target.startsWith("dvnote?")) {
		let notice_id = url_target.split("dvnote?")[1];
		insert_notice_one(notice_id);
	} else {
		insert_notice();
	}
}
// 존재하지 않는 공지사항
function Fail_notice_postOne() {
	Snackbar("존재하지않는 게시글입니다.");
	insert_notice();
}
// 공지사항 단일 포스트 반환 API
function Get_notice_postOne(id, callback) {
	$.when(A_JAX(host_ip+"/get_notice/"+id, "GET", null, null))
	.done(function (data) {
		if (data['result'] == 'success') {
			output =  JSON.parse(data['notice']);
			// 콜백함수, 인자로 User Information을 넣어준다.
			if (output == null) {
				Fail_notice_postOne();
			}
			if (typeof(callback) == 'function') {
				callback(output);
			}
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
			return false;
		}
	}).catch((data) => {
		Fail_notice_postOne();
		if (data.statue == 400) {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
}
// 공지사항 포스트 요청 API
function Get_notice_posts(callback) {
	$.when(A_JAX(host_ip+"/get_all_notice", "GET", null, null))
	.done(function (data) {
		if (data['result'] == 'success') {
			// 콜백함수, 인자로 User Information을 넣어준다.
			if (typeof(callback) == 'function') {
				callback(data);
			}
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
			return false;
		}
	}).catch((data) => {
		if(data.status == 400) {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
			return false;
		}
	});
}
// 공지사항 Components 구성
function insert_notice() {
	let target = $("#posts_target");
	//No_posts($("#posts_target"));	// 임시파일
	Get_notice_posts(function(result) {
		if (result) {
			let oid, title, phara, date, tag, activation = 0, activation_tag = ``;
			result = JSON.parse(result['notice_list']);
			save_posts = result.slice(30);
			result = result.slice(0, 30);
			Making_notice_block(result);	// 포스트 생성 및 삽입
		} else {
			// 에러 난 경우
			No_posts($("#posts_target"));
		}
	});
}
function Making_notice_block(posts) {
	let target = $("#posts_target");
	for (let post of posts) {
		oid = post['_id']['$oid'];
		title = post['title'];
		phara = post['post'];
		date = change_date_realative(post['date']['$date']);
		activation = post['activation'];
		if (activation == 1) {
			activation = `<span class="notice_post_activation noselect">[활성화] </span>`;
		} else activation = ``;
		tag =	`
					<div class="notice_post_container pointer" data-id=${oid} onclick="Click_post($(this))">
						<div class="notice_post_title_cont">
							<div class="notice_post_icon"></div>
							<div class="notice_post_title">${activation}${title}</div>
						</div>
						<div class="notice_post_date"><i class="far fa-clock"></i> ${date}</div>
						<div class="notice_post_post">${phara}</div>
					</div>
				`;
		target.append(tag);
	}
	$("#mobile_controller_none").addClass("display_none");
	$("#board_loading_modal").addClass("board_loading_modal_unvisible");
	$(".mobile_controller").removeAttr("style");
	$("#none_click").addClass("display_none");

	$("#menu_container").removeClass("menu_container_fixed");
	$("#posts_creating_loading").addClass("display_none");
	$("#board_container").removeClass("board_container_fixed");
}


// 공지사항 포스트 클릭
function Click_post(tag) {
	save_posts = [];
	now_topic = "개발자노트";
	where_topic = "개발자노트";
	now_state = "개발자노트";
	$("#board_info_board").text("SOOJLE");
	$("#board_info_text").text("개발자노트");
	$("#posts_target").empty();

	let target = tag.attr('data-id');
	location.href = "/board#dvnote?"+target;
}
// 공지사항 목록보기
function Notice_menu_btn() {
	location.href = "/board#dvnote";
}

// 단일 공지사항 표시
function insert_notice_one(id) {
	let target = $("#posts_target");
	target.empty();
	new Promise(function(resolve, reject) {
		Get_notice_postOne(id, function(result) {
			if (result) {
				let oid, title, phara, date, view, tag, activation = 0, activation_tag = ``;
				oid = result['_id']['$oid'];
				title = result['title'];
				phara = result['post'];
				view = result['view'];
				date = change_date_absolute(result['date']['$date']);
				activation = result['activation'];
				if (activation == 1) {
					activation_tag = `<span class="notice_post_activation noselect">[활성화] </span>`;
				}
				tag =	`
							<div id="notice_page_container" class="notice_page_container" data-id=${oid}>
								<div class="notice_page_upper_cont">
									<div class="notice_page_icon"></div>
									<div class="notice_page_title_cont">
										<div class="notice_page_title">${activation_tag} ${title}</div>
										<div class="notice_page_date"><i class="far fa-clock"></i> ${date} 작성됨</div>
									</div>
								</div>
								<div class="notice_page_view noselect">
								VIEW ${view}</div>
								<div id="notice_page_post" class="notice_page_post"><span style="font-weight:bold; font-size:22px;">${title}</span>\n\n${phara}</div>
								<div class="notice_menu_btn pointer" onclick="Notice_menu_btn()"><i class="fas fa-bars"></i> 목록보기</div>
							</div>
							<div id="notice_page_editor" class="notice_page_editor display_none"></div>
						`;
				target.append(tag);
			} else {
				No_posts($("#posts_target"));
			}
			$("#mobile_controller_none").addClass("display_none");
			$("#board_loading_modal").addClass("board_loading_modal_unvisible");
			$(".mobile_controller").removeAttr("style");
			$("#none_click").addClass("display_none");

			$("#menu_container").removeClass("menu_container_fixed");
			$("#posts_creating_loading").addClass("display_none");
			$("#board_container").removeClass("board_container_fixed");
			resolve();
		});
	}).then(function() {
		Check_ManagerInfo(function() {
			let tag = 	`
						<div class="notice_page_controll_cont">
							<div id="notice_page_edit" class="notice_page_edit pointer" onclick="Notice_Edit()">수정</div>
							<div id="notice_page_delete" class="notice_page_delete pointer" onclick="Notice_Delete()">삭제</div>
						</div>
						`;
			$("#notice_page_post").after(tag);
		});
	});
}

// 단일 공지사항 수정
function Notice_Edit() {
	Check_ManagerInfo(function() {
		$("#notice_page_container").addClass("display_none");
		$("#notice_page_editor").removeClass("display_none");
		let id = $("#notice_page_container").attr('data-id');
		let target = $("#notice_page_editor"), tag = ``;
		target.empty();
		Get_notice_postOne(id, function(result) {
			if (result) {
				tag = 	`
							<input id="notice_page_edit_title" class="notice_page_edit_title" placeholder="제목을 입력해주세요.">
							<textarea id="notice_page_edit_post" class="notice_page_edit_post" placeholder="${NOTICE_PLACEHOLDER}"></textarea>
							<div class="notice_page_controll_cont">
								<span class="activation_title noselect">공지 </span>
								<input type="checkbox" id="activation_toggle" name="activation_toggle">
								<div class="setting_toggle">
									<label for="activation_toggle"></label>
								</div>
								<div class="activatioin_info">공지를 선택할 시, 뉴스피드 상단에 노출됩니다.</div>
							</div>
							<div class="notice_page_controll_cont_edit">
								<div id="notice_page_edit_done" class="notice_page_edit_done pointer" onclick="Notice_Edit_Done()">완료</div>
								<div id="notice_page_edit_cancel" class="notice_page_edit_cancel pointer" onclick="Notice_Edit_Cancel()">취소</div>
							</div>
						`;
				target.append(tag);
				$("#notice_page_edit_title").val(result['title']);
				$("#notice_page_edit_post").val(result['post']);
				// 활성화 Check 유무
				if (result['activation'] == 1) {
					$("#activation_toggle").prop("checked", true);
				} else {
					$("#activation_toggle").prop("checked", false);
				}
			}
		});
	});
}
// 단일 공지사항 삭제
function Notice_Delete() {
	Check_ManagerInfo(function() {
		if (confirm("해당 게시글을 삭제하시겠습니까?")) {
			let id = $("#notice_page_container").attr("data-id");
			$.when(A_JAX(host_ip+"/remove_notice/"+id, "GET", null, null))
			.done(function(data) {
				if (data['result'] == "success") {
					alert("삭제 완료하였습니다.");
					location.replace("/board#dvnote");
				} else {
					Snackbar("잠시 후에 다시 시도해주세요!");
					return;
				}
			}).catch((data) => {
				if (data.status == 400) {
					Snackbar("잘못된 요청입니다.");
					return false;
				} else if (data.status == 403) {
					Snackbar("권한이 없습니다.");
					window.location.reload();
					return false;
				} else {
					Snackbar("서버와의 연결이 원활하지 않습니다.");
					return false;
				}
			});
		} 
	});
}
// 단일 공지사항 수정 완료
function Notice_Edit_Done() {
	Check_ManagerInfo(function() {
		let id = $("#notice_page_container").attr('data-id');
		let title = $("#notice_page_edit_title").val();
		let post = $("#notice_page_edit_post").val();
		let actiavation_check = 0
		if ($("#activation_toggle").is(":checked"))
			actiavation_check = 1;
		if (title.length == 0) {
			Snackbar("제목을 입력해주세요.");
			$("#notice_page_edit_title").focus();
			return;
		} else if (title.length > 50) {
			Snackbar("제목 길이 한계를 초과하였습니다.");
			$("#notice_page_edit_title").focus();
			return;
		}
		if (post.length == 0) {
			Snackbar("내용을 입력해주세요.");
			$("#notice_page_edit_post").focus();
			return;
		} else if (post.length > 1000) {
			Snackbar("내용 길이 한계를 초과하였습니다.");
			$("#notice_page_edit_post").focus();
			return;
		}
		let sendData = {
			'title': title,
			'post': post,
			'activation': actiavation_check
		};
		$.when(A_JAX(host_ip+"/update_notice/"+id, "POST", null, sendData))
		.done(function(data) {
			if (data['result'] == "success") {
				alert("수정 완료하였습니다.");
				location.reload();
			} else {
				Snackbar("잠시 후에 다시 시도해주세요!");
				return false;
			}
		}).catch((data) => {
			if (data.status == 400) {
				Snackbar("잘못된 요청입니다.");
				return false;
			} else if (data.status == 403) {
				Snackbar("권한이 없습니다.");
				window.location.reload();
				return false;
			} else {
				Snackbar("서버와의 연결이 원활하지 않습니다.");
				return false;
			}
		});
	});
}
// 단일 공지사항 수정 취소
function Notice_Edit_Cancel() {
	$("#notice_page_container").removeClass("display_none");
	$("#notice_page_editor").addClass("display_none");
}