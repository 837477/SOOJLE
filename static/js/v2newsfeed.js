function get_v2_posts(is_first = 0) {
	let token = sessionStorage.getItem('sj-state');
    if (token == null || token == undefined || token == 'undefined') {
    	Snackbar("로그인을 하면 맞춤서비스가 실행됩니다.");
    }
	menu_open = 0;
	out_of_search();
	window.scrollTo(0,0);
	now_topic = "추천";
	where_topic = "뉴스피드";
	posts_update = 0;
	now_state = now_topic;	// now state changing
	// 좌측 메뉴 버그 수정 fixed
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	$("#pc_search_input").val("");
	$("#mobile_search_input").val("");
	$("#board_info_text").text("SOOJLE의 추천");
	$("#board_info_board").text("뉴스피드");
	if (is_first == 1)
		menu_modal_onoff(2);
	else
		menu_modal_onoff();
	// 공지사항 삽입하기
	$("#posts_target").empty();
	Insert_Notice_Posts();
	$.when(A_JAX(host_ip+"/get_recommendation_newsfeed", "GET", null, null)).done(function (data) {
		if (now_topic != "추천") { return; }
		if (data['result'] == 'success') {
			let output = JSON.parse(data["newsfeed"]);
			if (output.length == 0)
				No_posts($("#posts_target"));
			save_posts = output.slice(30);
			output = output.slice(0, 30);
			if (token == null || token == undefined || token == 'undefined') {
		    	creating_post($("#posts_target"), output, "추천");
		    } else {
		    	console.log(output);
		    }
			$("html, body").animate({scrollTop: 0}, 400);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	}).catch(function(e) {
		Snackbar("잠시 후 다시 접속해주세요.");
	});
}