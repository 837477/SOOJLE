// Searchbar Task
let is_searching = 0;
let search_cache = "";	// 이전 검색어
let search_target = "";	// 목표 검색어
let now = 0;	// 현재 화살표로 선택한 div 위치
let all = 0;	// 검색결과 수
function search_focuson() {
	now = 0;
	let target = $("#search_recommend_box");
	if (mobilecheck()) {
		target = $("#mobile_search_recommend_box");
		$("#mobile_search_remcommend_box_container").removeClass("display_none");
		$("body").css("overflow", "hidden");
	} else {
		$("#search_remcommend_box_container").removeClass("display_none");
	}
	// 최근 검색어 표출
	Insert_user_recently_searchword(target);
}
function search_focus(keyCode, tag) {
	let target = $("#search_recommend_box");
	if (mobilecheck())target = $("#mobile_search_recommend_box")
	// 최근 검색어 표출
	//Insert_user_recently_searchword(target);

	if (keyCode == 13) {
		search_button();
		search_blur();
	} else if (keyCode == 38 || keyCode == 40) {
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
		// 문자열길이!=0, 문자열변화
		if (now_search.length != 0 && search_cache != now_search) {
			$(`.search_result:nth-child(${now})`).removeClass("search_target");
			now = 0;
			search_cache = tag.val();
			search_target = search_cache;
		} else if (tag.val() == "") {
			search_target = "";
			if (!mobilecheck()) {
				$("#search_remcommend_box_container").addClass("display_none");
				$(".search_result").remove();
			}
			let line = '<div class="search_loading pointer noselect" onclick="search_blur()">\
							<i class="fas fa-grip-lines"></i>\
						</div>';
			$("#mobile_search_recommend_box").append(line);
			search_cache = "";
		}
	}
}
function search_click() {
	if (mobilecheck()) {
		$("body").removeAttr("style");
		$("#mobile_search_remcommend_box_container").removeClass("display_none");
	} else {
		$("#search_remcommend_box_container").removeClass("display_none");
	}
}
function search_blur() {
	if (mobilecheck()) {
		$("body").removeAttr("style");
		$("#mobile_search_input").blur();
		$("#mobile_search_remcommend_box_container").addClass("display_none");
	} else {
		$("#pc_search_input").focusout();
		$("#search_remcommend_box_container").addClass("display_none");
	}
}

/*search 클릭 작업============================================================*/
function search_button() {	// 검색작업 data = 글자
	let data;
	if (mobilecheck()) {
		data = $("#mobile_search_input").val();
		search_blur();
		$("body").removeAttr("style");
		search_open = 0;
	} else {
		data = $("#pc_search_input").val();
	}
	if (data == ""){
		Snackbar("검색어를 입력해주세요.");
		is_searching = 0;
		return;
	} else if (data.length > 200) {
		data = data.slice(0, 200);
	}
	data = data.replace(/ /g, "+");
	window.location.href = "/board#search?" + data + '/'
}
let search_open = 0;
function mobile_search_modal_open() {
	if (search_open == 0) {
		if (grid_open == 1)
			grid_modal_off();
		if (menu_open == 1)
			menu_modal_off();
		if (mobilecheck()) {
			scroll(0,0);
			$("#board_logo").css({"left": "10px",
								"transform": "translate(0, 0)",
								"-webkit-transform": "translate(0, 0)"});
			$("body").css({"position": "fixed","overflow": "hidden"});
			$("#mobile_search").removeClass("display_none");
			$("#mobile_search_input").focus();
			search_open = 1;
			$("#mobile_search_remcommend_box_container").removeClass("display_none");
		}
	} else {
		if (mobilecheck() && $("#mobile_search_input").val() != "") {
			mobile_search_modal_close();
			// $("#mobile_search_input").focus();
			// $("#mobile_search_remcommend_box_container").removeClass("display_none");
		}
		else if (mobilecheck()) {
			mobile_search_modal_close();
		}
	}
}
function mobile_search_modal_close() {
	search_open = 0;
	$("body").removeAttr("style");
	$("#mobile_search_remcommend_box_container").addClass("display_none");
	$("#board_logo").removeAttr("style");
	$("#mobile_search").addClass("display_none");
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
$(document).on('touchend', function(e) {
	if (search_open == 1) {
		if ($(e.target.classList)[0]  == 'mobile_search_header' ||	// nothing
			$(e.target.classList)[0] == 'mobile_search_button_modal' ||
			$(e.target.classList)[0] == 'result_target' ||
			$(e.target.classList)[0] == 'mobile_search_input' ||
			$(e.target.classList)[0] == 'mobile_search_icon_modal' ||
			$(e.target.classList)[0] == 'search_recommend_box' ||
			$(e.target.classList)[0] == 'search_result') {
		} else if (mobilecheck() && $("#mobile_search_input").val() != "") {
			$("body").removeAttr("style");
			$("#mobile_search_input").blur();
		}
	}
});

// 검색 api 실행 함수
let similarity_words;
let domain_posts = [];
let a_jax_posts = [];
/*
0: 최근 트렌드
1: 대학교
2: 동아리&모임
3: 공모전&행사
4: 진로&구인
5: 자유
6: 예외
*/
function search_text(text) {
	a_jax_posts = [];
	domain_posts = [];
	now_state = text;
	let now_creating_state = now_state;
	// 좌측 메뉴 버그 수정 fixed
	$("#menu_container").removeAttr("style");
	$("#menu_container").removeClass("menu_container_fixed");
	// 현재 검색 중이면 차단
	if (is_searching == 1) return;
	is_searching = 1;
	if (text == ""){
		Snackbar("검색어를 입력해주세요.");
		is_searching = 0;
		return;
	} 
	// search_input box text input
	if (mobilecheck()) {
		$("#mobile_search_input").val(text.replace(/\+/g, " "));
	} else {
		$("#pc_search_input").val(text.replace(/\+/g, " "));
	}
	$("#posts_creating_loading").removeClass("display_none");
	$("#posts_target").empty();
	search_container_set();
	now_topic = "검색 결과입니다!";
	where_topic = "SOOJLE 엔진";
	posts_update = 0;
	$("#board_info_text").empty();
	$("#board_info_text").text("검색 결과입니다!");
	$("#board_info_board").empty();
	$("#board_info_board").text("SOOJLE 엔진");
	let category_tabs = `<div class="category_tabs">
							<div id="category0" class="category_tab pointer category_checked" onclick="category_select($(this))">통합 검색</div>\
							<div id="category1" class="category_tab pointer" onclick="category_select($(this))">최근 트렌드</div>\
							<div id="category2" class="category_tab pointer" onclick="category_select($(this))">대학교</div>\
							<div id="category3" class="category_tab pointer" onclick="category_select($(this))">동아리&모임</div>\
							<div id="category4" class="category_tab pointer" onclick="category_select($(this))">공모전&행사</div>\
							<div id="category5" class="category_tab pointer" onclick="category_select($(this))">진로&구인</div>\
							<div id="category6" class="category_tab pointer" onclick="category_select($(this))">자유</div>\
							<div id="category7" class="category_tab category_tab_last pointer" onclick="category_select($(this))">일반</div>\
							<div class="search_option_btn pointer" onclick="Search_Option()"><i class="fas fa-ellipsis-h"></i></div>\
						</div>`;
	$("#posts_target").append(category_tabs);
	let search_option_div = `
								<div id="search_option_container" class="search_option_container display_none">
									<div class="search_option_title noselect">검색옵션</div>
									<div id="search_option_sort_date" class="search_option_sort pointer" onclick="Search_Option_Sort_Date()">
										<div class="search_option_round"></div>
										<span>최신순</span>
									</div>
									<div id="search_option_sort_relevance" class="search_option_sort pointer search_option_select" onclick="Search_Option_Sort_Relevance()">
										<div class="search_option_round"></div>
										<span>관련도순</span>
									</div>
								</div>
							`;
	$("#posts_target").append(search_option_div);
	$("#posts_target").append(`<div id="search_posts_target"></div>`);
	let send_data = {};
	send_data["search"] = text.trim().toLowerCase();
	send_data["opiton"] = {
		"sort": 'trend'
	}
	Search_logging(send_data["search"]);				// 검색 Logging API 호출
	Get_Search_Posts(send_data, now_creating_state);	// 검색 API 호출
	Search_Option_on();									// 검색 옵션 오픈
	// 연관검색어 임시중지
	// $.when(A_JAX(host_ip+"/get_similarity_words", "POST", null, send_data)).done(function (data) {
	// 	if (data['result'] == "success") {
	// 		similarity_words = data['similarity_words'];
	// 		insert_recommend_words(data['similarity_words'], now_creating_state);
	// 	} else {
	// 		Snackbar("다시 접속해주세요!");
	// 	}
	// });
}
// 검색 로깅 API 호출
function Search_logging(text) {
	let sendData = {'search': text};
	A_JAX(host_ip+"/search_logging", "POST", null, sendData);
}
// 검색 API 호출
function Get_Search_Posts(sendData, now_creating_state) {
	a_jax_posts[0] = [];
	$.when(A_JAX(host_ip+"/domain_search", "POST", null, sendData))
	.done(function (data) {
		if (data['result'] == 'success') {
			domain_posts = data["search_result"];
			insert_domain_post(data["search_result"], now_creating_state);
		}
	});
	$.when(
		$.when(A_JAX(host_ip+"/category_search/대학교/200", "POST", null, sendData))
		.done((data) => {
			if (data['result'] == "success") {
				let output = remove_duplicated(1, data["search_result"]);
				a_jax_posts[1] = output;
			}
		}).catch((e) => {
			// Ajax fail
		}),
		$.when(A_JAX(host_ip+"/category_search/동아리&모임/200", "POST", null, sendData))
		.done(function (data) {
			if (data['result'] == "success") {
				let output = remove_duplicated(2, data["search_result"]);
				a_jax_posts[2] = output;
			}
		}).catch((e) => {
			// Ajax fail
		}),
		$.when(A_JAX(host_ip+"/category_search/공모전&행사/200", "POST", null, sendData))
		.done(function (data) {
			if (data['result'] == "success") {
				let output = remove_duplicated(3, data["search_result"]);
				a_jax_posts[3] = output;
			}
		}).catch((e) => {
			// Ajax fail
		}),
		$.when(A_JAX(host_ip+"/category_search/진로&구인/200", "POST", null, sendData))
		.done(function (data) {
			if (data['result'] == "success") {
				let output = remove_duplicated(4, data["search_result"]);
				a_jax_posts[4] = output;
			}
		}).catch((e) => {
			// Ajax fail
		}),
		$.when(A_JAX(host_ip+"/category_search/자유/200", "POST", null, sendData))
		.done(function (data) {
			if (data['result'] == "success") {
				let output = remove_duplicated(5, data["search_result"]);
				a_jax_posts[5] = output;
			}
		}).catch((e) => {
			// Ajax fail
		}),
		$.when(A_JAX(host_ip+"/category_search/예외/200", "POST", null, sendData))
		.done(function (data) {
			if (data['result'] == "success") {
				let output = remove_duplicated(6, data["search_result"]);
				a_jax_posts[6] = output;
			}
		}).catch((e) => {
			// Ajax fail
		})
	).then(() => {
		// 각 카테고리 게시물에서 similarity가 가장 높은 200개 Trend로 선정
		Create_trend_posts();
		check_search_results_sort();
	}).then(() => {
		$("#posts_creating_loading").addClass("display_none");
		Do_Like_Sign();			// 좋아요 표시
		result_search_zero();	// 검색결과 0개일경우
		
	});
}
// 검색 창 구성 함수
function search_container_set() {
	let domain_target = `<div id="sr_dt"></div>`;
	let search_recommend_target = `<div id="sr_recommend" class="sr_recommend"></div>`;
	let target = $("#search_posts_target");
	// 연관검색어 임시중지
	//target.append(search_recommend_target);
	target.append(domain_target);
}
// 도메인 검색 결과를 해당 div에 넣어줌
function insert_domain_post(posts, now_creating_state = "") {
	let id, title, phara, url, post_one, domain_block;
	let domain_target = `<div id="sr_dt"></div>`;
	$("#search_posts_target").append(domain_target);
	let target = $("#sr_dt");
	let domain_tag = `
		<div class="sr_title">웹사이트</div>`;
	let line = `<div class="sr_line"></div>`;
	posts = posts.slice(0, 5);
	for (post_one of posts) {
		url = post_one["url"];
		title = post_one["title"];
		if (title.length > 45) {
			title = title.slice(0,45) + " ...";
		}
		phara = post_one["post"];
		if (phara.length > 70) {
			phara = phara.slice(0,70) + " ...";
		}
		domain_block = `
			<div class="sr_domain_ct" p-id="0">
				<a href = ${url} target="_blank">
					<div>
						<div class="sr_domain_title">${title}</div>
						<div class="sr_domain_url">${url}</div>
						<div class="sr_domain_post">${phara}</div>
					</div>
				</a>
				<div>
					<div class="post_menu" onclick="post_menu_open($(this))"><i class="fas fa-ellipsis-h"></i></div>
				</div>
			</div>`;
		domain_tag += domain_block;
	}
	domain_tag += line;
	if (posts.length == 0) {
		target.remove();
	}
	else {
		target.append(domain_tag); 
	}
}
/*
0: 최근 트렌드
1: 대학교
2: 동아리&모임
3: 공모전&행사
4: 진로&구인
5: 자유
6: 예외
*/
// 검색 결과를 해당 div에 넣어줌
function insert_search_post(target_num, posts, now_creating_state = "", is_fav_cnt = 1) {
	a_jax_posts[target_num] = posts;		// posts 저장
	let posts_len = 0;
	if (posts == undefined) posts_len = 0;
	else {
		posts_len = posts.length;
		posts = posts.slice(0,5); // 미리보기는 5개까지만 보여줌
	}
	let target = $("#search_posts_target"), target_name = target_num;
	if (Number(target_name) == 0) {target_name = "최근 트렌드";}
	else if (Number(target_name) == 1) {target_name = "대학교";}
	else if (Number(target_name) == 2) {target_name = "동아리&모임";}
	else if (Number(target_name) == 3) {target_name = "공모전&행사";}
	else if (Number(target_name) == 4) {target_name = "진로&구인";}
	else if (Number(target_name) == 5) {target_name = "자유";}
	else {target_name = "일반";}
	let target_tag = `<div class="sr_title noselect">${target_name}</div>`;
	creating_post($("#search_posts_target"), posts, now_creating_state, is_fav_cnt, function(tag_str) {
		let line = `<div class="sr_line"></div>`;
		let more;
		if (posts_len == 0) { return; }
		else if (posts_len < 6) {more = ``;}
		else {more = `<div class="sr_more" onclick="more_posts(${target_num})">더 보기 <i class="far fa-arrow-alt-circle-right"></i></div>`;}
		tag_str = target_tag + tag_str + more + line;
		if (now_creating_state == now_state){
			target.append($(tag_str));
		}
	});
}
// 연관 검색어 삽입
function insert_recommend_words(words_dict, now_creating_state = "") {
	let target = $("#sr_recommend");
	let recommends = [];
	let output = [];
	let words_key, words_list, word;
	for (words_key in words_dict) {
		words_list = words_dict[words_key];
		for (word of words_list) {
			recommends.push(word);
		}
	}
	recommends.sort(compare);
	recommends = recommends.slice(0, 6);
	for (word of recommends) {
		output.push(Object.keys(word)[0]);
	}
	if (output.length == 0) {
		target.remove();
		return;
	}
	let title = `<div class="sr_recommend_word_title noselect">이런 검색어는 어떤가요?</div>`;
	if (now_creating_state == now_state)
		target.append(title);
	for (word of output) {
		words_key = `<div class="sr_recommend_word" onclick="recommend_word_click($(this))">${word}</div>`;
		if (now_creating_state == now_state)
			target.append(words_key);
	}
}
function compare( a, b ) {
  if ( Object.values(a)[0] > Object.values(b)[0] ){
    return -1;
  }
  if ( Object.values(a)[0] < Object.values(b)[0] ){
    return 1;
  }
  return 0;
}
function recommend_word_click(tag) {
	let text = tag.text();
	if (is_searching == 1) {
		return;
	}
	search_text(text);
	$("#mobile_search_input").val(text);
	$("#pc_search_input").val(text);
}

// 검색결과 페이지에서 카테고리 선택
function more_posts(target_num, is_fav_cnt = 1) {
	$(".category_checked").removeClass("category_checked");
	$(`#category${target_num + 1}`).addClass("category_checked");
	let target_name = target_num;
	if (Number(target_name) == 0) {target_name = "최근 트렌드";}
	else if (Number(target_name) == 1) {target_name = "대학교";}
	else if (Number(target_name) == 2) {target_name = "동아리&모임";}
	else if (Number(target_name) == 3) {target_name = "공모전&행사";}
	else if (Number(target_name) == 4) {target_name = "진로&구인";}
	else if (Number(target_name) == 5) {target_name = "자유";}
	else {target_name = "일반";}
	let more_left_tag = `<img src="/static/icons/back.png" class="sr_more_to_before noselect" onclick="Click_before_posts_pc()">${target_name}`;
	$("#board_info_text").empty();
	$("#board_info_text").append(more_left_tag);
	if (a_jax_posts[target_num] != undefined && a_jax_posts[target_num].length == 0) return false;	// 아무 포스트가 없음
	let now_creating_state = now_state;
	window.scroll(0, 0);
	$("#menu_container").removeAttr("style");
	$("#search_posts_target").empty();

	save_posts = a_jax_posts[target_num];	///////////////////
	let posts = save_posts.slice(0,30);		/*	 30개 분할   */
	save_posts = save_posts.slice(30);		//////////////////
	creating_post($("#search_posts_target"), posts, now_creating_state, is_fav_cnt);

	setTimeout(function() {
		if (!mobilecheck()) {
			$("#menu_container").removeAttr("style");//.removeClass("menu_container_searching");
		}
	}, 1000);
}
// 검색 카테고리 페이지에서 뒤로가기 클릭
function before_posts() {
	$(".category_checked").removeClass("category_checked");
	$("#category0").addClass("category_checked");
	$("#posts_creating_loading").removeClass("display_none");
	$("#search_posts_target").empty();
	// 연관검색어 임시중지
	//$("#search_posts_target").append(`<div id="sr_recommend" class="sr_recommend"></div>`);
	$("#board_info_text").empty();
	$("#board_info_text").text("검색 결과입니다!");
	$("#board_info_board").empty();
	$("#board_info_board").text("SOOJLE 엔진");
	//search_container_set();
	// 연관검색어 임시중지
	insert_recommend_words(similarity_words, now_state);
	insert_domain_post(domain_posts, now_state);
	for (let i = 0; i< 7; i++) {
		if (sum[i] != 0){
			insert_search_post(index[i], a_jax_posts[index[i]], now_state);
		}
	}
	result_search_zero();	// 통합 검색 결과 0개
	Do_Like_Sign();			// 로딩 제거
	is_searching = 0;
	$("#posts_creating_loading").addClass("display_none");
}
// PC 검색 카테고리 페이지에서 뒤로가기 클릭
function Click_before_posts_pc() {
	if (mobilecheck()) return;
	else before_posts();
}
// 중복게시글 삭제
function remove_duplicated(target, posts) {
	let output = [], index = [], post_one, i, j, posts_len = posts.length;
	for (i = 0; i < posts_len; i++) index.push(0);
	for (i = posts_len - 1; i >= 0; i--) {
		for (j = i - 1; j >= 0; j--) {
			if (posts[i]["_id"] == posts[j]["_id"]) {
				index[i] = 1;
				break;
			} else if (posts[i]["similarity"] != posts[j]['similarity']){
				break;
			}
		}
	}
	for (i = 0; i < posts_len; i++) {
		if (index[i] == 1) continue;
		output.push(posts[i]);
	}
	return output;
}
// 트렌드 게시물 제작
function Create_trend_posts() {
	a_jax_posts[0] = [];
	let index = [0], max = 0, cnt = 0;
	for (let i = 1; i < a_jax_posts.length; i++)
		index.push(0)
	while (cnt < 200) {
		target = 0;
		max = 0;
		for (let i = 1; i < a_jax_posts.length; i++) {
			if (a_jax_posts[i][index[i]] == undefined) continue;
			if (a_jax_posts[i][index[i]]['similarity'] > max) {
				target = i;
				max = a_jax_posts[i][index[i]]['similarity'];
			}
		}
		if (target == 0) break;
		a_jax_posts[0].push(a_jax_posts[target][index[target]]);
		index[target] += 1;
		cnt++;
	}
}
// 통합 검색 결과 0개
function result_search_zero() {
	let s = 0;
	for (let a_jax_posts_one of a_jax_posts)
		s += a_jax_posts_one.length;
	if (s == 0) {
		No_posts($("#search_posts_target"));
	}
}

// 연산
function similarity_sort(index, sum) {
	let i, j, max, tmp;
	for (i = 0; i< 5; i++) {
		max = i;
		for (j = i + 1; j< 5; j++)
			if (sum[max] < sum[j])
				max = j;
		if (max != i) {
			tmp = sum[i];
			sum[i] = sum[max];
			sum[max] = tmp;
			tmp = index[i];
			index[i] = index[max];
			index[max] = tmp;
		}
	}
	return index;
}
let index = [0, 1, 2, 3, 4, 5, 6], sum = [0, 0, 0, 0, 0, 0, 0];
function check_search_results_sort() {
	idx = [0, 1, 2, 3, 4, 5, 6];
	for (let i = 0; i < 7; i++) {
		if (a_jax_posts[i] != undefined){
			for (let j = 0; j<7; j++){
				if (a_jax_posts[i][j] != undefined)
					sum[i] += a_jax_posts[i][j]["similarity"];
			}
		}
	}
	index = similarity_sort(idx, sum);
	for (let i = 0; i< 7; i++) {
		insert_search_post(index[i], a_jax_posts[index[i]], now_state);
	}
	Do_Like_Sign();			// 로딩 제거
	is_searching = 0;
	$("#posts_creating_loading").addClass("display_none");
}
// 카테고리 선택
function category_select(tag) {
	let id = tag.attr('id');
	if (id == 'category0') {
		if (tag.hasClass('category_checkd')) return;
		else before_posts();
	} else {
		if (more_posts(Number(id.slice(8)) - 1) == false) {
			No_posts($("#search_posts_target"));
		}
	}
}

// 검색 창 끄기
function out_of_search() {
	search_open = 1;
	$("#mobile_search_input").val("");
	$("#pc_search_input").val("");
	mobile_search_modal_close();
}


let search_option_open = false;

// 검색 옵션========================================================================
function Search_Option_on() {	// PC 라면 옵션 자동 On
	if (!mobilecheck()) {
		search_option_open = !search_option_open;
		$("#search_option_container").removeClass("display_none");
	}
}
function Search_Option() {
	if (search_option_open) {
		search_option_open = !search_option_open;
		$("#search_option_container").addClass("display_none");
	} else {
		search_option_open = !search_option_open;
		$("#search_option_container").removeClass("display_none");
	}
}
// 최신순 정렬
function Search_Option_Sort_Date() {
	let date_sort = $("#search_option_sort_date").hasClass("search_option_select");
	if (!date_sort) {
		$("#search_option_sort_relevance").removeClass("search_option_select");
		$("#search_option_sort_date").addClass("search_option_select");
		for (let i in a_jax_posts) {
			a_jax_posts[i].sort(function(a, b){
				return new Date(b.date) - new Date(a.date);
			});
		}
	}
	Search_Option_Sort();
}
// 관련도순 정렬
function Search_Option_Sort_Relevance() {
	let relevance_sort = $("#search_option_sort_relevance").hasClass("search_option_select");
	if (!relevance_sort) {
		$("#search_option_sort_relevance").addClass("search_option_select");
		$("#search_option_sort_date").removeClass("search_option_select");
		for (let i in a_jax_posts) {
			a_jax_posts[i].sort(function(a, b){
				return b.similarity - a.similarity;
			});
		}
	}
	Search_Option_Sort();
}
// 정렬된 데이터 적용
function Search_Option_Sort() {
	let target = $(".category_checked").text();
	// 변경된 순서 적용
	if (target == "통합 검색") {
		before_posts();
	} else if (target == "최근 트렌드") {
		category_select($("#category1"));
	} else if (target == "대학교") {
		category_select($("#category2"));
	} else if (target == "동아리&모임") {
		category_select($("#category3"));
	} else if (target == "공모전&행사") {
		category_select($("#category4"));
	} else if (target == "진로&구인") {
		category_select($("#category5"));
	} else if (target == "자유") {
		category_select($("#category6"));
	} else if (target == "일반") {
		category_select($("#category7"));
	} 
}