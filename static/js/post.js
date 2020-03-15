let save_posts = [];
let posts_update = 1;
var now_topic;
var where_topic;

// 게시글이 없을 때, 실행
function No_posts(target) {
	target.empty();
	$("#posts_creating_loading").addClass("display_none");
	let imoticon = imoticons[Math.floor(Math.random() * imoticons.length)];
	//<img src="./static/image/none_posts.png" class="sr_none_posts_img">
	let no_posts_tag = `
		<div class="sr_none_posts_cont">
			<div class="sr_none_posts_img noselect">${imoticon}</div>
			<div class="sr_none_posts_text">포스트가 존재하지 않습니다!</div>
		</div>`;
	target.append(no_posts_tag);
}
// 추천 뉴스피드 불러오기 함수
function click_recommend_posts() {
	location.replace("/board#recommend");
	menu_modal_onoff();
}
function get_recommend_posts(is_first = 0) {
	menu_open = 0;
	out_of_search();
	window.scrollTo(0,0);
	now_topic = "추천";
	where_topic = "뉴스피드";
	posts_update = 0;
	now_state = now_topic;	// now state changing
	//location.replace("/board#recommend");
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
	Insert_Notice_Posts();
	$.when(A_JAX(host_ip+"/get_recommendation_newsfeed", "GET", null, null)).done(function (data) {
		if (data['result'] == 'success') {
			let output = JSON.parse(data["newsfeed"]);
			if (output.length == 0)
				No_posts($("#posts_target"));
			save_posts = output.slice(30);
			output = output.slice(0, 30);
			creating_post($("#posts_target"), output, "추천");
			$("html, body").animate({scrollTop: 0}, 400);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	}).catch(function(e) {
		Snackbar("잠시 후 다시 접속해주세요.");
	});
}
// 인기 뉴스피드 불러오기 함수
function click_popularity_posts() {
	location.replace("/board#popularity");
	menu_modal_onoff();
}
function get_popularity_posts() {
	menu_open = 0;
	out_of_search();
	window.scrollTo(0,0);
	now_topic = "인기";
	where_topic = "뉴스피드";
	posts_update = 0;
	now_state = now_topic;	// now state changing
	location.replace("/board#popularity");
	// 좌측 메뉴 버그 수정 fixed
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	$("#pc_search_input").val("");
	$("#mobile_search_input").val("");
	$("#board_info_text").empty();
	$("#board_info_text").text("인기");
	$("#board_info_board").empty();
	$("#board_info_board").text("뉴스피드");
	// 공지사항 삽입하기
	Insert_Notice_Posts();
	let a_jax = A_JAX(host_ip+"/get_popularity_newsfeed", "GET", null, null);
	$.when(a_jax).done(function () {
		let json = a_jax.responseJSON;
		if (json['result'] == 'success') {
			let output = JSON.parse(json["newsfeed"]);
			save_posts = output.slice(30);
			output = output.slice(0, 30);
			creating_post($("#posts_target"), output, "인기");
			$("html, body").animate({scrollTop: 0}, 400);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	});
}
function click_topic_posts(tag) {
	let topic_click = '';
	if (typeof(tag) == String || typeof(tag) == "string") topic_click = tag;
	else topic_click = tag.children('div').text();
	location.replace(`/board#topic?${topic_click}`);
	menu_modal_onoff();
}
// 토픽별 뉴스피드 불러오기 함수
function get_topic_posts(tag) {
	menu_open = 0;
	out_of_search();
	window.scrollTo(0,0);
	where_topic = "뉴스피드";
	posts_update = 0;
	let topic;
	if (typeof(tag) == String || typeof(tag) == "string") topic = tag;
	else topic = tag.children('div').text();
	now_topic = topic;
	now_state = now_topic;	// now state changing
	// 좌측 메뉴 버그 수정 fixed
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	$("#pc_search_input").val("");
	$("#mobile_search_input").val("");
	$("#board_info_text").empty();
	$("#board_info_text").text(topic);
	$("#board_info_board").empty();
	$("#board_info_board").text("뉴스피드");
	// 공지사항 삽입하기
	Insert_Notice_Posts();
	let a_jax = A_JAX(host_ip+"/get_newsfeed_of_topic/"+topic, "GET", null, null);
	$.when(a_jax).done(function () {
		let json = a_jax.responseJSON;
		if (json['result'] == 'success') {
			let output = JSON.parse(json["newsfeed"]);
			if (output.length == 0) {
				No_posts($("#posts_target"));

			} else {
				save_posts = output.slice(30);
				output = output.slice(0, 30);	
				creating_post($("#posts_target"), output, topic);
			}
			$("html, body").animate({scrollTop: 0}, 400);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	});
}
// 스크롤 이벤트
let now_creating = 0;
let header_scrolling = 0;
$(document).scroll(function() {
	if (!mobilecheck() && $(window).scrollTop() == 0) {
		$("#menu_container").removeAttr("style").css("transition", "0s ease-in-out");
	} else if (!mobilecheck() && $(window).scrollTop() > 60) {
		$("#menu_container").css("top", "30px");
		if (header_scrolling == 0) {
			$("#menu_container").css("transition", ".2s ease-in-out");	
			header_scrolling = 1;
		}
		setTimeout(function() {$("#menu_container").css("transition", "0s ease-in-out")}, 400);
	}
	else if (!mobilecheck() && $(window).scrollTop() < 60) {
		$("#menu_container").removeAttr("style").css("transition", ".2s ease-in-out");
		header_scrolling = 0;
	}
	if (where_topic == "뉴스피드" 
		|| (where_topic == "SOOJLE 엔진" && $("#board_info_text").text() != "검색 결과입니다!")
		|| where_topic == "개발자노트"){

		if ($(window).scrollTop() + $(window).height() >= $(document).height() - 200){
			if (save_posts.length == 0) return;
			if (now_creating == 0) {
				now_creating = 1;
				$("#posts_creating_loading").removeClass("display_none");
				//$("#board_container").addClass("board_container_fixed");
				setTimeout(function() {
					if (where_topic == "뉴스피드")
						get_posts_more(now_state, $("#posts_target"));
					else if (where_topic == "개발자노트")
						get_notices_more();
					else
						get_posts_more(now_state, $("#search_posts_target"));
					setTimeout(function() {
						now_creating = 0;
					}, 200);
				}, 600);
			}
		}
	}
});
// 포스트 더보기
function get_posts_more(before_state, target) {
	if (save_posts.length == 0) return;
	setTimeout(function() {
		let output = save_posts.slice(0,30);
		save_posts = save_posts.slice(30);
		creating_post(target, output, before_state);
	}, 0);
}
// 공지사항 더보기
function get_notices_more() {
	if (save_posts.length == 0) return;
	setTimeout(function() {
		let output = save_posts.slice(0,30);
		save_posts = save_posts.slice(30);
		Making_notice_block(output);
	}, 0);
}


// 포스트 메뉴 열기
function post_menu_open(tag) {
	let id = tag.parent('div').attr("p-id");
	let url = tag.parent('div').children('a').attr("href");
	if (url == undefined) {
		url = tag.parent('div').parent('div').children('a').attr("href");
	}
	$("body").css("overflow", "hidden");
	$("#post_menu_modal_container").attr("p-id", id);
	$("#post_menu_modal_container").attr("p-url", url);
	$("#post_menu_modal_container").removeClass("display_none");
	$("#post_menu_modal").removeClass("display_none");
	$("#post_menu_modal").addClass('fadeIn');
	setTimeout(function() {
		$("#post_menu_modal").removeClass('fadeIn');
	}, 1000);
}
// 포스트 메뉴 닫기
function post_menu_close() {
	$("body").removeAttr("style");
	$("#post_menu_modal_container").addClass("display_none");
	$("#post_menu_modal").addClass("display_none");
}

// 포스트 url 복사
function post_url_copy(tag) {
	Snackbar("URL 복사가 완료되었습니다!");
	let url = tag.parent('div').parent('div').attr("p-url");
	let id = tag.parent('div').parent('div').attr("p-id");
	let output = $(`<input type="text" class="copy_input" value="${url}">`);
	$("body").append(output);
	output.select();
	document.execCommand('Copy');
	output.remove();
	post_menu_close();
	// API 호출
	A_JAX(host_ip+"/post_view/"+id, "GET", null, null);
}
// 포스트 페이스북 공유
function Share_facebook(tag) {
	let url = tag.parent('div').parent('div').attr("p-url");
	window.open('http://www.facebook.com/sharer/sharer.php?u='+url, '_blank');
}
// 포스트 트위터 공유
function Share_twitter(tag) {
	let url = tag.parent('div').parent('div').attr("p-url");
	window.open('https://twitter.com/home?status='+url, '_blank');
}


// 좋아요 애니메이션 동작함수
function post_like_animation(tag) {
	tag = tag.parent('div').parent('div');
	let box = $(document.createElement("div"));
	box.addClass("like_animation wow animated bounceIn");
	box.attr("data-wow-duration", "0.6s");
	let icon = $(document.createElement("i"));
	icon.addClass("fas fa-heart");
	box.append(icon);
	tag.append(box);
	setTimeout(function() {
		box.removeClass("wow bounceIn");
		box.removeAttr("style");
		box.addClass("bounceOut");
		setTimeout(function() {
			box.remove();
		}, 800);
	}, 1000);
}
// 좋아요 버튼 함수
function post_like_button(tag) {
	let id = tag.parent('div').parent('div').attr("p-id");	// 다시 재지정해주기
	let is_like = tag.attr("ch");
	if (Number(is_like) == 0) {
		tag.attr("ch", "1");
		post_like_animation(tag);
		post_like(id, tag);
	} else {
		tag.attr("ch", "0");
		tag.removeAttr("style");
		post_dislike(id, tag);
	}
}
// 좋아요 실행 함수
function post_like(id, tag) {
	let token = sessionStorage.getItem('sj-state');
	if (token == null){
		Snackbar("로그인이 필요합니다.");
		return;
	}
	$.when(A_JAX(host_ip+"/post_like/"+id, "GET", null, null))
	.done((data) => {
		if (data['result'] == 'success') {
			tag.css("color", "#f00730");
			let cnt = Number(tag.next('div').text());
			cnt += 1;
			tag.next('div').empty();
			tag.next('div').text(cnt.toString());
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
	}).catch((data) => {
		if (data.status == 400) {
			Snackbar("잠시 후 다시 시도해주세요.");
		} else if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		}
	});
}
// 좋아요 취소 함수
function post_dislike(id, tag) {
	let token = sessionStorage.getItem('sj-state');
	if (token == null){
		Snackbar("로그인이 필요합니다.");
		return;
	}
	$.when(A_JAX(host_ip+"/post_unlike/"+id, "GET", null, null))
	.done((data) => {
		if (data['result'] == 'success') {
			tag.removeAttr("style");
			let cnt = Number(tag.next('div').text());
			cnt -= 1;
			tag.next('div').empty();
			tag.next('div').text(cnt.toString());
		} else {
			Snackbar("잠시 후 다시 시도해주세요.");
		}
	}).catch((data) => {
		if (data.status == 400) {
			Snackbar("잠시 후 다시 시도해주세요.");
		} else if (data.status == 401) {
			Snackbar("다시 로그인 해주세요.");
			sessionStorage.removeItem('sj-state');
			localStorage.removeItem('sj-state');
		} else {
			Snackbar("서버와의 연결이 원활하지 않습니다.");
		}
	});
}


// 포스트 링크 클릭 함수
let mouse_which = 1;
$(document).ready(function(){
	$(".post_block").mousedown(function(e) {
		mouse_which = e.which; // 1:좌클릭, 2:휠클릭, 3:우클릭
	});
});
function post_view(tag) {
	if ((mobilecheck() && tag.parent('a').attr("href").indexOf("educe") != -1) ||
		(mobilecheck() && tag.parent('a').attr("href").indexOf("thinkcontest") != -1)) {
		alert("해당 사이트는 모바일에서 정상적인 접속이 되지않을 수도 있습니다.")
			window.open(tag.parent('a').attr("href"), '_blank');	
	}
	// 위의 document ready 함수의 속도를 위해서 지연시간 400 설정
	setTimeout(function() {
		if (mouse_which == 3) return;
		let id = tag.parent('a').parent('div').attr("p-id");
		let e = mouse_which;
		if (e == 1 || e == 2) {
			A_JAX(host_ip+"/post_view/"+id, "GET", null, null);
		}
	}, 400);
}

// 몇일전 몇분전 표기
function change_date_realative(dt) {
	let min = 60 * 1000;
	let c = new Date()
	let d = new Date(dt);
	d.setHours(d.getHours() - 9);
	let minsAgo = Math.floor((c - d) / (min));
	let result = {
		'raw': d.getFullYear() + '-' + 
		(d.getMonth() + 1 > 9 ? '' : '0') + (d.getMonth() + 1) + '-' + 
		(d.getDate() > 9 ? '' : '0') +  d.getDate() + ' ' + 
		(d.getHours() > 9 ? '' : '0') +  d.getHours() + ':' + 
		(d.getMinutes() > 9 ? '' : '0') +  d.getMinutes() + ':'  + 
		(d.getSeconds() > 9 ? '' : '0') +  d.getSeconds(),
		'formatted': '',
		'string_raw': d.getFullYear() + '년 ' + 
		/*(d.getMonth() + 1 > 9 ? '' : '0') +*/ (d.getMonth() + 1) + '월 ' + 
		/*(d.getDate() > 9 ? '' : '0') +*/  d.getDate() + '일'
	};
	if (c.getFullYear() == d.getFullYear()) {
		result['string_relative'] = (d.getMonth() + 1) + '월 ' + d.getDate() + '일'
	} else {
		result['string_relative'] = result.string_raw;
	}
	if (minsAgo < 60 && minsAgo >= 0) { 										// 1시간 내
		result.formatted = minsAgo + '분 전';
	} else if (minsAgo < 60 * 24 && minsAgo >= 0) { 							// 하루 내
		result.formatted = Math.floor(minsAgo / 60) + '시간 전';
	} else if (minsAgo < 60 * 25 * 7 && minsAgo >= 0) {							// 7일 내
		result.formatted = Math.floor(minsAgo / 60 / 24) + '일 전 ';
	} else if (minsAgo < 60 * 25 * 7 * 4 && minsAgo >= 0) {						// 한달 내
		result.formatted = Math.floor(minsAgo / 60 / 24 / 7) + '주 전 ';
	} else if (minsAgo < 60 * 25 * 7 * 4 * 13 && minsAgo >= 0) {				// 1년 내
		result.formatted = Math.floor(minsAgo / 60 / 24 / 7 / 4) + '개월 전 ';
	} else if (minsAgo >= 0) { 													// 1년 이상
		result.formatted = Math.floor(minsAgo / 60 / 24 / 7 / 4 / 12) + '년 전 ';
	}
	 else {																	// 현재 이후
		result.formatted = result.string_raw + "까지";
	}
	return result.formatted;
}
function change_date_absolute(dt) {
	let d = new Date(dt);
	let result = {
		'raw': d.getFullYear() + '-' + 
		(d.getMonth() + 1 > 9 ? '' : '0') + (d.getMonth() + 1) + '-' + 
		(d.getDate() > 9 ? '' : '0') +  d.getDate() + ' ' + 
		(d.getHours() > 9 ? '' : '0') +  d.getHours() + ':' + 
		(d.getMinutes() > 9 ? '' : '0') +  d.getMinutes() + ':'  + 
		(d.getSeconds() > 9 ? '' : '0') +  d.getSeconds()
	}
	return result.raw;
}
// yyyyMMddHHmmss 형태로 포멧팅하여 날짜 반환
Date.prototype.SetTime = function()
{
    let yyyy = this.getFullYear().toString();
    let MM = (this.getMonth() + 1).toString();
    let dd = this.getDate().toString();
    this.setHours(this.getHours() - 9);
    let HH = this.getHours().toString();
    let mm = this.getMinutes().toString();
    let ss = this.getSeconds().toString();
    return yyyy + "." + 
    		(MM[1] ? MM : '0'+ MM[0]) + "." + 
    		(dd[1] ? dd : '0'+ dd[0]) + " " +
    		(HH[1] ? HH : '0'+ HH[0]) + ":" + 
    		(mm[1] ? mm : '0'+ mm[0]) + ":" + 
    		(ss[1] ? ss : '0'+ ss[0]);
}
// 3000년 게시글인지 확인 : Custom 기능
function IsContest(dt) {
	let d = new Date(dt);
	if (d.getFullYear() == 3000) return false;
	return true;
}
// 게시글 제작 함수
function creating_post(target_tag, posts, now_creating_state = "", is_fav_cnt = 1, callback) {
	let target = target_tag;
	new Promise(function(resolve, reject) {
		$("#posts_creating_loading").removeClass("display_none");
		if (mobilecheck()) Creating_mobile_post(posts, '', is_fav_cnt, function(result){ resolve(result); });
		else Creating_pc_post(posts, '', is_fav_cnt, function(result){ resolve(result); });
	}).then((result) => {
		if (now_creating_state == now_state){
			if (typeof(callback) == 'function') {
				callback(result);					// For Search Functin
			} else {
				target.append($(result));			// For Others
				Do_Like_Sign();
			}
		}
	}).then(() => {
		$("#mobile_controller_none").addClass("display_none");
		$("#board_loading_modal").addClass("board_loading_modal_unvisible");
		$(".mobile_controller").removeAttr("style");
		$("#none_click").addClass("display_none");

		$("#menu_container").removeClass("menu_container_fixed");
		$("#posts_creating_loading").addClass("display_none");
		$("#board_container").removeClass("board_container_fixed");
	});
}
// 모바일 태그 만들기
function Creating_mobile_post(posts = [], target_tag = '', is_fav_cnt, callback) {
	let check, contest_check = false;
	let id, fav_cnt, title, date, end_date, url, domain, img, subimg, tag, post_one, fav_cnt_block, contest_block;
	for (let post_one of posts) {
		contest_check = false;
		check = 0;
		if (post_one['_id'].$oid) id = post_one['_id'].$oid;
		else id = post_one['_id'];
		fav_cnt = post_one['fav_cnt'];
		title = post_one['title'];
		if (title.length > 45) {
			title = title.slice(0,45) + " ...";
		}
		if (post_one['date'].$date) date = post_one['date'].$date;
		else date = post_one['date'];
		if (post_one['end_date']) {
			if (post_one['end_date'].$date) end_date = post_one['end_date'].$date;
			else end_date = post_one['end_date'];
			if (IsContest(end_date)) {					// 공모전 게시글 판별
				contest_check = true;
				date = change_date_realative(end_date);
			} else {
				date = change_date_realative(date);
			}
		} else {
			date = change_date_realative(date);
		}
		url = post_one['url'];
		domain = url.split('/');
		domain = domain[0] + '//' + domain[2];
		img = post_one['img'];
		if (is_fav_cnt == 1) {
			fav_cnt_block = `<div class="post_like_cnt">${fav_cnt}</div>`;
		} else {
			fav_cnt_block = ``;
		}
		if (contest_check == true) {
			if (new Date(end_date) > new Date(Date.now())) {
				contest_block = `<div class="contest_ing">진행중</div>`;
			} else {
				contest_block = `<div class="contest_done">마감</div>`;
			}
		} else {
			contest_block = ``;
		}
		if (img.toString().indexOf("everytime") != -1) {
			img = "./static/image/everytime.jpg";
			check = 1;
		} else if (img.toString().indexOf("daum") != -1) {
			img = "./static/image/sjstation.png";
			check = 1;
		}
		if (img.length < 10 || img.length == undefined && check == 0) {
			tag = `<div class="post_block" p-id="${id}">
					<a href="${url}" target="_blank">
						<div class="post_title_cont_noimg pointer" onmousedown="post_view($(this))">
							<div class="post_title">${title}</div>
						</div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_block_cont_noimg pointer" onmousedown="post_view($(this))">
							<div class="post_url">${domain}</div>
							<div class="post_date"><i class="far fa-clock"></i> ${date}${contest_block}</div>
						</div>
					</a>
					<div class="post_block_set_cont_noimg noselect">
						<div class="post_like" ch="0" onclick="post_like_button($(this))"><i class="far fa-heart"></i></div>
						${fav_cnt_block}
					</div>
					<div class="post_menu noselect" onclick="post_menu_open($(this))"><i class="fas fa-ellipsis-h"></i></div>
				</div>`
		} else {
			tag = `<div class="post_block" p-id="${id}">
					<a href="${url}" target="_blank">
						<div class="post_title_cont pointer" onmousedown="post_view($(this))">
							<div class="post_title">${title}</div>
						</div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_block_img_cont" onmousedown="post_view($(this))" style="background-image: url('${img}')"></div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_block_cont pointer" onmousedown="post_view($(this))">
							<div class="post_url">${domain}</div>
							<div class="post_date"><i class="far fa-clock"></i> ${date}${contest_block}</div>
						</div>
					</a>
					<div class="post_block_set_cont noselect">
						<div class="post_like" ch="0" onclick="post_like_button($(this))"><i class="far fa-heart"></i></div>
						${fav_cnt_block}
					</div>
					<div class="post_menu " onclick="post_menu_open($(this))"><i class="fas fa-ellipsis-h"></i></div>
				</div>`
		}
		target_tag += tag;
		check_image(tag);
	}
	// Callback Function
	if (typeof(callback) == 'function') {
		callback(target_tag);
	}
	return target_tag;
}
// PC 태그 만들기
function Creating_pc_post(posts = [], target_tag = '', is_fav_cnt, callback) {
	let check, contest_check = false;
	let id, fav_cnt, title, date, end_date, url, domain, img, subimg, tag, post_one, fav_cnt_block, contest_block;
	for (let post_one of posts) {
		if (post_one == undefined)
			continue;
		contest_check = false;
		check = 0;
		if (post_one['_id'].$oid) id = post_one['_id'].$oid;
		else id = post_one['_id'];
		fav_cnt = post_one['fav_cnt'];
		title = post_one['title'];
		if (title.length > 50) {
			title = title.slice(0,50) + " ...";
		}
		if (post_one['date'].$date) date = post_one['date'].$date;
		else date = post_one['date'];
		if (post_one['end_date']) {
			if (post_one['end_date'].$date) end_date = post_one['end_date'].$date;
			else end_date = post_one['end_date'];
			if (IsContest(end_date)) {					// 공모전 게시글 판별
				contest_check = true;
				date = change_date_realative(end_date);
			} else {
				date = change_date_realative(date);
			}
		} else {
			date = change_date_realative(date);
		}
		url = post_one['url'];
		domain = url.split('/');
		domain = domain[0] + '//' + domain[2];
		img = post_one['img'];
		if (is_fav_cnt == 1) {
			fav_cnt_block = `<div class="post_like_cnt">${fav_cnt}</div>`;
		} else {
			fav_cnt_block = ``;
		}
		if (contest_check == true) {
			if (new Date(end_date) > new Date(Date.now())) {
				contest_block = `<div class="contest_ing">진행중</div>`;
			} else {
				contest_block = `<div class="contest_done">마감</div>`;
			}
		} else {
			contest_block = ``;
		}
		if (img.toString().indexOf("everytime") != -1) {
			img = "./static/image/everytime.jpg";
			check = 1;
		} else if (img.toString().indexOf("daum") != -1) {
			img = "./static/image/sjstation.png";
			check = 1;
		}
		if (img.length < 10 || img.length == undefined && check == 0) {
			tag = `<div class="post_block" p-id="${id}">
					<a href="${url}" target="_blank">
						<div class="post_title_cont_noimg pointer" onmousedown="post_view($(this))">
							<div class="post_title">${title}</div>
						</div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_block_cont_noimg pointer" onmousedown="post_view($(this))">
							<div class="post_url">${domain}</div>
							<div class="post_date"><i class="far fa-clock"></i> ${date}${contest_block}</div>
						</div>
					</a>
					<div class="post_block_set_cont_noimg noselect">
						<div class="post_like" ch="0" onclick="post_like_button($(this))"><i class="far fa-heart"></i></div>
						${fav_cnt_block}
					</div>
					<div class="post_menu " onclick="post_menu_open($(this))"><i class="fas fa-ellipsis-h"></i></div>
				</div>`
		} else {
			tag = `<div class="post_block" p-id="${id}">
					<a href="${url}" target="_blank">
						<div class="post_block_img_cont" onmousedown="post_view($(this))" style="background-image: url('${img}')"></div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_title_cont pointer" onmousedown="post_view($(this))">
							<div class="post_title">${title}</div>
						</div>
					</a>
					<a href="${url}" target="_blank">
						<div class="post_block_cont pointer" onmousedown="post_view($(this))">
							<div class="post_url">${domain}</div>
							<div class="post_date"><i class="far fa-clock"></i> ${date}${contest_block}</div>
						</div>
					</a>
					<div class="post_block_set_cont noselect">
						<div class="post_like" ch="0" onclick="post_like_button($(this))"><i class="far fa-heart"></i></div>
						${fav_cnt_block}
					</div>
					<div class="post_menu " onclick="post_menu_open($(this))"><i class="fas fa-ellipsis-h"></i></div>
				</div>`
		}
		target_tag += tag;
		check_image(tag);
	}
	// Callback Function
	if (typeof(callback) == 'function') {
		callback(target_tag);
	}
	return target_tag;
}
// 게시글에 좋아요 표시 함수
function Do_Like_Sign() {
	let token = sessionStorage.getItem('sj-state');
	if (token == null || token == undefined || token == 'undefined') {}
	else {
		Get_UserInfo(function(result) {
			if (result) {
				let posts = $(".post_block");
				let post_one;
				for (post_one of posts) {
					for (let fav_post of result["user_fav_list"]) {
						if ($(post_one).attr("p-id") == fav_post["_id"]) {
							$(post_one).children('div').children('div.post_like').css("color", "#f00730");
							$(post_one).children('div').children('div.post_like').attr("ch", "1");
						}
					}
				}
			}
		});
	}
}
function check_image(tag) {
	let onerror = `./static/image/shortcut_black_mobile.png`;
	if ($(tag).find("div.post_block_img_cont") == undefined) return false;
	if ($(tag).find("div.post_block_img_cont").css("background-image") == undefined) return false;
	let img_url = $(tag).find("div.post_block_img_cont").css("background-image").slice(5, -2);
	let checkimg = new Image();
	let p_id = $(tag).attr("p-id");
	checkimg.onerror = function() {
		try {
			$("#posts_target").find(`div[p-id=${p_id}]`).find("div.post_block_img_cont").css("background-image", `url(${onerror})`);
		} catch(e) {
			console.log(e);
		}
	}
	checkimg.onload = function() {
		// Image Loading Success
	}
	checkimg.src = img_url;
}

/* 
0 : 좋아요, 뷰, 검색
1 : 좋아요
2 : 뷰
3 : 검색
*/
// 좋아요 게시물 보기
function click_user_like_posts() {
	menu_modal_onoff();
	location.replace("/board#userlike");
}
function get_user_like_posts() {
	out_of_search();
	window.scroll(0,0);
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	now_topic = "관심 게시글";
	where_topic = "내 정보";
	now_state = now_topic;
	let now_creating_state = now_state;
	posts_update = 0;
	menu_modal_onoff();
	$("#board_info_text").empty();
	$("#board_info_text").text("관심 게시글");
	$("#board_info_board").empty();
	$("#board_info_board").text("내 정보");
	// 좋아요 게시글 반환
	Get_Like_Post(function(posts) {
		if (posts.length == 0) {
			$("#menu_container").addClass("menu_container_searching");
			$("#menu_container").removeAttr("style");
			let target = $("#posts_target");
			let imoticon = imoticons[Math.floor(Math.random() * imoticons.length)];
			//<img src="./static/image/none_posts.png" class="sr_none_posts_img">
			let no_posts_tag = `
				<div class="sr_none_posts_cont">
					<div class="sr_none_posts_img noselect">${imoticon}</div>
					<div class="sr_none_posts_text">관심있는 게시글이 없네요!</div>
				</div>`;
			if (now_creating_state == now_state)
				target.append(no_posts_tag);
			$("#posts_creating_loading").addClass('display_none');
			$("#board_container").removeClass("board_container_fixed");
			$("#menu_container").removeClass('menu_container_searching');
			$("#menu_container").removeClass('menu_container_fixed');
		} else {
			save_posts = posts.slice(30);
			posts = posts.slice(0, 30);
			creating_post($("#posts_target"), posts, now_creating_state, 0);
		}
	});
}
// 최근 본 게시물 보기
function click_user_view_posts() {
	menu_modal_onoff();
	location.replace("/board#userview");
}
function get_user_view_posts() {
	out_of_search();
	window.scroll(0,0);
	$("#menu_container").addClass("menu_container_fixed");
	$("#posts_creating_loading").removeClass("display_none");
	$("#board_container").addClass("board_container_fixed");
	$("#posts_target").empty();
	now_topic = "최근 본 게시글";
	where_topic = "내 정보";
	now_state = now_topic;
	let now_creating_state = now_state;
	posts_update = 0;
	menu_modal_onoff();
	$("#board_info_text").empty();
	$("#board_info_text").text("최근 본 게시글");
	$("#board_info_board").empty();
	$("#board_info_board").text("내 정보");
	// 최근 본 게시글 반환
	Get_Recently_View_Post(function(posts) {
		if (posts.length == 0) {
			$("#menu_container").addClass("menu_container_searching");
			$("#menu_container").removeAttr("style");
			let target = $("#posts_target");
			let imoticon = imoticons[Math.floor(Math.random() * imoticons.length)];
			//<img src="./static/image/none_posts.png" class="sr_none_posts_img">
			let no_posts_tag = `
				<div class="sr_none_posts_cont">
					<div class="sr_none_posts_img noselect">${imoticon}</div>
					<div class="sr_none_posts_text">관심있는 게시글이 없네요!</div>
				</div>`;
			if (now_creating_state == now_state)
				target.append(no_posts_tag);
			$("#posts_creating_loading").addClass('display_none');
			$("#board_container").removeClass("board_container_fixed");
			$("#menu_container").removeClass('menu_container_searching');
			$("#menu_container").removeClass('menu_container_fixed');
		} else {
			save_posts = posts.slice(30);
			posts = posts.slice(0, 30);
			creating_post($("#posts_target"), posts, now_creating_state, 0);
		}
	});
}

// 공지사항 상단에 추가하기
function Insert_Notice_Posts() {
	let target = $("#posts_target");
	Get_notice_posts(function(result) {
		if (result) {
			result = JSON.parse(result['notice_list']);
			result = result.reverse();
			let oid, title, post, div;
			for (post of result) {
				oid = post['_id']['$oid'];
				title = post['title'];
				activation = post['activation'];
				if (activation == 1) {
					div = 	`
								<div class="board_notice_cont pointer" data-id="${oid}" onclick="Click_post($(this))">
									<span class="notice_post_activation">[공지] </span>
									${title}
								</div>
							`;
					target.prepend(div);
				}
			}
		}
	});
}