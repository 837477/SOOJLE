function Go_lab() {
	location.href = "/board#lab";
	out_of_search();
	now_topic = "Lab";
	where_topic = "Lab";
	now_state = "Lab";
	$("#board_info_board").text("수즐 연구소");
	$("#board_info_text").text("Lab");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);
	menu_modal_onoff();
	set_lab();
	insert_lab_service();
}
function Go_service(tag) {
	let url = $(tag).attr("target");
	window.open('about:blank').location.href = url;
}
function number_plus_comma(num) {
	num = num.toString();
	let output = "";
	for (let i = num.length - 1; i >= 0; i--) {
		if ((num.length - i - 1) % 3 == 0 && num.length - 1 != i)
			output = num[i] + ',' + output;
		else
			output = num[i] + output;
	}
	return output;
}
function service_like_button(tag) {
	let id = $(tag).parent('div').attr("id_");
	let num = Number($(tag).find(".lab_service_choice_number").text().replace(/,/gi, ""));
	let output = "";
	// 서비스 관심 취소
	if ($(tag).find(".lab_service_choice_content").hasClass("lab_service_choice_content_checked")){
		$(tag).find(".lab_service_choice_content").removeClass("lab_service_choice_content_checked");
		num = (num - 1);
		output = number_plus_comma(num);
		$(tag).find(".lab_service_choice_number").text(output);
	// 서비스 관심 동작
	} else {
		$(tag).find(".lab_service_choice_content").addClass("lab_service_choice_content_checked");
		num = (num + 1);
		output = number_plus_comma(num);
		$(tag).find(".lab_service_choice_number").text(output);
		/*$.when(
			A_JAX(host_ip+"/post_like/"+id, "GET", null, null)
		).done(function(data) {
			if (data.responseJSON['result'] == 'success') {

			} else {
				Snackbar("서버와의 통신이 원활하지 않습니다.");
				num = (num - 1);
				output = number_plus_comma(num);
				$(tag).find(".lab_service_choice_number").text(output);
			}
		});*/
	}
}

function set_lab() {
	let div = 	`<div class="lab_title_wrap">
					<div class="lab_title noselect">수즐 연구소에 오신 것을 환영합니다.</div>
					<div class="lab_subtitle noselect">
						세종대학교 여러분에게 새로운 경험을 드리겠습니다.
					</div>
				</div>`;
	$("#posts_target").append(div);
	$("#posts_creating_loading").addClass("display_none");
}

function insert_lab_service() {
	let div =	`<div id="lab_service_contents_wrap" class="lab_service_contents_wrap">
					<div class="lab_category_title noselect">새로운 서비스를 도전!</div>
					<div class="lab_category_subtitle noselect">수즐팀 또는 인재들의 야심찬 서비스입니다.</div>
				</div>
				<div id="lab_function_contents_wrap" class="lab_service_contents_wrap">
					<div class="lab_category_title noselect">새로운 기능을 도전!</div>
					<div class="lab_category_subtitle noselect">수즐을 좀 더 재미있게 만들기 위한 수즐팀의 도전 기능입니다.</div>
				</div>`;
	$("#posts_target").append(div);
	set_lab_service();
	set_lab_function();
}
function set_lab_service() {
	let title = `모닥불`;
	let subtitle = `세종대학교소프트웨어융합대학 홈페이지 2020 개편.`;
	let content = 	`<div class="lab_service_content noselect" id_="31bB8df00fdi9fdf121">
						<div class="lab_service_info_wrap pointer" onclick="Go_service(this)" target="https://bonfire-2.gitbook.io/modakbul/">
							<div class="lab_service_content_img_wrapper">
								<img class="lab_service_content_img" src="./static/saves/modakbul.png">
							</div>
							<div class="lab_service_content_title">${title}</div>
							<div class="lab_service_content_subtitle">${subtitle}</div>
						</div>
						<div class="lab_service_choice_wrap pointer" onclick="service_like_button(this)">
							<div class="lab_service_choice_number">1,470</div>
							<div class="lab_service_choice_content">좋은 기능이에요.</div>
						</div>
					</div>`;
	//$("#lab_service_contents_wrap").append(content);
	let nothing =	`<div class="lab_nothing noselect">
						더 나은 서비스를 위해 준비중입니다.
					</div>`;
	$("#lab_service_contents_wrap").append(nothing);
}
function set_lab_function() {
	let nothing =	`<div class="lab_nothing noselect">
						더 나은 서비스를 위해 준비중입니다.
					</div>`;
	$("#lab_function_contents_wrap").append(nothing);
}