let analysis_data = {};
const time_event = {
					'1225': `<span style="color: green">행복한</span> <span style="color:red">메리크리스마스!</span>`,
					'11': `새해<span style="font-weight:bold; color:red;">복</span> 많이 받으세요!`,
					'1224': `<span style="color:red">크리스마스</span>를 <span style="color:green">준비</span>하세요!`,
					'1111': `11월 11일은 <span sytle="font-weight:bold">'가래떡데이'</span>랍니다.`,
					'55': `<span style="color:green">동심</span>으로 돌아가볼까요?`,
					'214': `카카오 100% 함유 <span color="green">초콜릿</span>은 어떤가요?`,
					'31': `3.1절의 정식명칭은 <span style="font-weight:bold">독립선언일</span>이라는거 알고계셨나요?`,
					'66': `애국선열과 국군장병들의 충절을 추모합니다`,
					'815': `<span style="font-weight:bold">광복절.</span> 대한민국 독립일`,
					'103': `단군이 고조선을 처음 건국한 날입니다.`,
					'109': `한국어는 자랑스러운 <span style="color:red">대한민국</span>의 언어입니다.`,
					'314': `달콤한 <span color="green">사탕</span>.. 저도 먹고싶네요!`
				}

function Click_analysistic() {

	location.href = "/board#analysistics";
	if (menu_open == 1) {
		menu_modal_onoff();
	}
}

function Go_analysistic() {
	out_of_search();
	now_topic = "통계";
	where_topic = "통계";
	now_state = "통계";
	$("#board_info_board").text("SOOJLE 애널리틱스");
	$("#board_info_text").text("통계");
	$("#posts_target").empty();
	$("#posts_creating_loading").removeClass("display_none");
	window.scrollTo(0,0);
	menu_modal_onoff();
	set_analysistic();
}

function set_analysistic() {
	$.when(A_JAX(host_ip+"/get_analysis", "GET", null, null))
	.done(function(data) {
		if (data['result'] == 'success') {
			analysis_data = data['analysis'];
			let div = `<div id="anlt_time_weather_wrap" class="anlt_time_weather_wrap"></div>`;
			$("#posts_target").append(div);
			$("#posts_creating_loading").addClass("display_none");
			insert_greeting_div();			// 소개
			insert_time_div();				// 시간
			insert_realtimesearch_div();	// 실시간 검색어
			//insert_hall();				// 명예의 전당
			insert_visitor_div();			// 방문자 분석
			insert_post_div();				// 게시글 분석
			//insert_outlink_div();			// 외부사이트 분석
			insert_device_div();			// 디바이스 분석
		}
	});
}

// 소개 div Insert----------------------------------------------------
function insert_greeting_div() {
	let posts_num = analysis_data['posts_count'];
	let actions_num = analysis_data['communication_avg'];// /86400.toFixed(0); // 1일 == 86400초
	let view_num = analysis_data['total_view'];
	let div =	`<div id="anlt_greeting_wrapper" class="anlt_greeting_wrapper">
					<div class="anlt_greeting_text noselect">
						사용자는 <span style="font-weight:500; color: #12b886;">${number_unit(posts_num)}</span> 개의 포스트에서 정보를 찾아볼 수 있습니다.
					</div>\
					<div class="anlt_greeting_text noselect">
						사용자와 SOOJLE은 하루 평균 <span style="font-weight:500; color: #12b886;">${number_unit(actions_num)}</span> 번의 소통을 하고있습니다.
					</div>\
					<div class="anlt_greeting_text noselect">
						사용자들은 SOOJLE을 통해서 <span style="font-weight:500; color: #12b886;">${number_unit(view_num)}</span> 번의 정보를 찾았습니다.
					</div>\
				</div>`;
	let m_div = `<div id="anlt_greeting_wrapper" class="anlt_greeting_wrapper">
					<div class="anlt_greeting_text noselect">
						SOOJLE 정보량 <span style="font-weight:500; color: #12b886;">${number_unit(posts_num)}</span>
					</div>\
					<div class="anlt_greeting_text noselect">
						SOOJLE과의 1초 평균 <span style="font-weight:500; color: #12b886;">${number_unit(actions_num)}</span> 번의 소통
					</div>\
					<div class="anlt_greeting_text noselect">
						<span style="font-weight:500; color: #12b886;">${number_unit(view_num)}</span> 번의 정보 이용
					</div>\
				</div>`;
	if (mobilecheck()) $("#posts_target").append(m_div);
	else $("#posts_target").append(div);
	greeting_enlargement();
}
let greeting_anlt_num = 0;
function greeting_enlargement() {
	$(".anlt_greeting_text").removeClass("anlt_greeting_text_checked");
	$(".anlt_greeting_text").eq(greeting_anlt_num).addClass('anlt_greeting_text_checked');
	setTimeout(function() {
		greeting_anlt_num = (greeting_anlt_num + 1) % 3;
		greeting_enlargement();
	}, 3000);
}

// 시각 div Insert----------------------------------------------------
function insert_time_div() {
	let div = `
				<div class="anlt_time_wrap">
					<div id="anlt_time_yymmdd" class="anlt_time_yymmdd noselect"></div>
					<div id="anlt_time_ampm" class="anlt_time_ampm noselect"></div>
					<div id="anlt_time_hhmmss" class="anlt_time_hhmmss noselect"></div>
					<div id="anlt_time_event" class="anlt_time_event noselect"></div>
				</div>
			`;
	$("#anlt_time_weather_wrap").append(div);
	set_analysistic_time();
}
function addZeros(num, digit) { // 자릿수 맞춰주기
	let zero = '';
	num = num.toString();
	if (num.length < digit) {
		for (i = 0; i < digit - num.length; i++) {
			zero += '0';
		}
	}
	return zero + num;
}
function set_analysistic_time() {
	let day_name = ["일", "월", "화", "수", "목", "금", "토"];
	if (now_topic != "통계") return;
	let time = new Date();
	let year = time.getFullYear();
	let month = time.getMonth() + 1;
	let date = time.getDate();
	let day = time.getDay();
	let hour = addZeros(time.getHours(),2); 
	let minute = addZeros(time.getMinutes(),2);
	let second = addZeros(time.getSeconds(),2);
	let ampm = "AM";
	set_analysistic_time_event(month, date);
	if (hour > 12) {
		hour -= 12;
		ampm = "PM";
	}
	else ampm = "AM";
	let now_date = year + '-' + month + '-' + date + " " + day_name[day] + "요일";
	let now_time = hour + ':' + minute + ':' + second;
	$("#anlt_time_yymmdd").text(now_date);
	$("#anlt_time_hhmmss").text(now_time);
	$("#anlt_time_ampm").text(ampm);
	setTimeout(function() {set_analysistic_time()}, 1000);
}
function set_analysistic_time_event(month, date) {
	let event = time_event[month.toString()+date.toString()];
	if (event != null){
		$("#anlt_time_event").empty();
		$("#anlt_time_event").append(event);
	}
	else
		$("#anlt_time_event").empty();
}

// 실시간 검색어 div Insert---------------------------------------------
function insert_realtimesearch_div() {
	let info = `SOOJLE에서 가장 인기있는 검색어를 실시간으로 보여드립니다.`;
	let div = 	`
					<div id="anlt_realtime_wrap" class="anlt_realtime_wrap">
						<div class="anlt_realtime_title noselect">실시간 검색어</div>\
						<div class="anlt_realtime_subtitle noselect">${info}</div>\
						<div class="anlt_reatime_words_wrap">\
							<div id="anlt_reatime_word_1to5" class="anlt_reatime_word_elements">\
							</div><div id="anlt_reatime_word_6to10" class="anlt_reatime_word_elements"></div>\
						</div>
						<div id="anlt_realtime_standard" class="anlt_realtime_standard noselect"></div>
					</div>
				`;
	$("#posts_target").append(div);
	set_realtimesearch();
}
function set_realtimesearch() {
	let realtime_words_list;
	$.when(A_JAX(host_ip+"/get_search_realtime", "GET", null, null))
	.done(function (data) {
		if (data['result'] == 'success') {
			realtime_words_list = data['search_realtime'];
			let target, div, i;
			for (i = 1; i <= realtime_words_list.length; i++) {
				let word;
				if (realtime_words_list[i - 1] != undefined) {
					word = realtime_words_list[i - 1][0];
					if (i == 1) {
						div = `<div class="anlt_realtime_word pointer" onclick="realtime_word_search($(this))">\
									<span class="anlt_realtime_word_num noselect">${i}</span>
									<span class="anlt_realtime_word_real" style="color:#c30e2e">${word}</span>\
								</div>`;
					}
					else {
						div = `<div class="anlt_realtime_word pointer" onclick="realtime_word_search($(this))">\
									<span class="anlt_realtime_word_num noselect">${i}</span>
									<span class="anlt_realtime_word_real">${word}</span>\
								</div>`;
					}
					if (i < 6) target = $('#anlt_reatime_word_1to5');
					else target = $("#anlt_reatime_word_6to10");
					target.append(div);
				}
			}
		} else {
			Snackbar("실시간 검색어를 불러오지 못하였습니다.");
		}
	});
	let date = $("#anlt_time_yymmdd").text();
	let ampm = $("#anlt_time_ampm").text();
	let time = $("#anlt_time_hhmmss").text();
	let standard = `${date} ${ampm} ${time} 기준`;
	$("#anlt_realtime_standard").append(standard);
}
function realtime_word_search(tag) {
	let text = tag.text().trim().slice(4);
	//search_text(text);
	window.location.href = `/board#search?${text}/`;
}

// 명예의 전당 div Insert-------------------------------------------------
function insert_hall() {
	let info = `사용자들이 SOOJLE에서 최고 기록을 갱신하신 분야에 대해서 분석해드립니다.`;
	let div = 	`
				<div id="anlt_postdata_wrap" class="anlt_visitor_wrap">
					<div class="anlt_visitor_title noselect">명예의 전당</div>\
					<div class="anlt_realtime_subtitle noselect">${info}</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">외부사이트</div>
						<div id="anlt_outlink_text_max_data" class="anlt_top_text_data">대양휴머니티칼리지</div>
					</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">학과/학부</div>
						<div id="anlt_major_text_max_data" class="anlt_top_text_data">컴퓨터공학과</div>
					</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">학번</div>
						<div id="anlt_number_text_max_data" class="anlt_top_text_data">16학번</div>
					</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">검색어</div>
						<div id="anlt_search_text_max_data" class="anlt_top_text_data">수강편람</div>
					</div>\
				</div>
	`;
	$("#posts_target").append(div);
	set_hall_data();
}
function set_hall_data() {

}

// 방문자 분석 div Insert-----------------------------------------------
function insert_visitor_div() {
	let info = `SOOJLE의 모든 방문자들의 통계를 분석하여 보여드립니다.`;
	let div = 	`
					<div id="anlt_visitor_wrap" class="anlt_visitor_wrap">
						<div class="anlt_visitor_title noselect">방문자 분석</div>\
						<div class="anlt_realtime_subtitle noselect">${info}</div>\
						<div class="anlt_visitor_box noselect">
							<div class="anlt_visitor_box_title">오늘 방문자수</div>
							<div id="anlt_today_visitor_data" class="anlt_visitor_box_data">${number_unit(analysis_data['today_visitor'])}</div>
						</div>\
						<div class="anlt_visitor_box noselect">
							<div class="anlt_visitor_box_title">총 방문자수</div>
							<div id="anlt_all_visitor_data" class="anlt_visitor_box_data">${number_unit(analysis_data['total_visitor'])}</div>
						</div>\
						<div class="anlt_visitor_box noselect">
							<div class="anlt_visitor_box_title">하루 평균 방문자수</div>
							<div id="anlt_today_visitor_average_data" class="anlt_visitor_box_data">${number_unit(analysis_data['day_avg_visitor'])}</div>
						</div>\
						<div class="anlt_visitor_box noselect">
							<div class="anlt_visitor_box_title">하루 최고 방문자수</div>
							<div id="anlt_all_visitor_max_data" class="anlt_visitor_box_data">${number_unit(analysis_data['highest_day_visitor'])}</div>
						</div>\
						<div class="anlt_visitor_chart_box">
							<div class="anlt_visitor_box_title_big noselect">사용 시간대 분석</div>
							<canvas id="visitor_distribution" class="anlt_visitor_chart_element" width="auto" height="auto"></canvas>
						</div>\
					</div>
				`;
	$("#posts_target").append(div);
	set_visitor_data();
}
function set_visitor_data() {
	let visitor_time_data, visitor_number_data, vistior_time;
	$.when(A_JAX(host_ip+"/get_everyday_analysis_days_ago/"+2, "GET", null, null))
	.done(function (data) {
		if (data['result'] == 'success') {
			let visitor_time_data_array1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]; 
			let visitor_time_data_array2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,];
			let visitor_time_data1, visitor_time_data2, visitor_time_date1, visitor_time_date2;
			if (data['analysis'][0] != undefined) {
				visitor_time_data1 = data['analysis'][0]['today_time_visitor'];
				visitor_time_date1 = data['analysis'][0]['date'];
				let now_time = new Date(visitor_time_date1);
				visitor_time_date1 = `${now_time.getMonth() + 1}월 ${now_time.getDate()}일`;
				for (let st in visitor_time_data1)
					visitor_time_data_array1[visitor_time_data1[st]['time'] - 1] = visitor_time_data1[st]['visitor'];
			}
			if (data['analysis'][1] != undefined) {
				visitor_time_data2 = data['analysis'][1]['today_time_visitor'];
				visitor_time_date2 = data['analysis'][1]['date'];
				let now_time = new Date(visitor_time_date2);
				visitor_time_date2 = `${now_time.getMonth() + 1}월 ${now_time.getDate()}일`;
				for (let st in visitor_time_data2)
					visitor_time_data_array2[visitor_time_data2[st]['time'] - 1] = visitor_time_data2[st]['visitor'];
			}
			get_line("visitor_distribution",
				[	// visitor date
					visitor_time_date1,
					visitor_time_date2 
				],
				[	// visitor data
					visitor_time_data_array1,
					visitor_time_data_array2
				],
			);
		} else {
			Snackbar("방문자 데이터를 가져오지 못하였습니다.");
		}
	});
}

// 게시글 분석 div Insert------------------------------------------------
function insert_post_div() {
	let info = `게시글에 대한 전체 통계를 분석해 보여드립니다.`;
	let div = 	`
				<div id="anlt_postdata_wrap" class="anlt_visitor_wrap">
					<div class="anlt_visitor_title noselect">게시글 분석</div>\
					<div class="anlt_realtime_subtitle noselect">${info}</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">전체 게시글 조회 수</div>
						<div id="anlt_all_posts_view_data" class="anlt_visitor_box_data">${number_unit(analysis_data['total_view'])}</div>
					</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">전체 게시글 공감 수</div>
						<div id="anlt_all_posts_like_data" class="anlt_visitor_box_data">${number_unit(analysis_data['total_fav'])}</div>
					</div>\
				</div>
	`;
	$("#posts_target").append(div);
	set_post_data();
}
function set_post_data() {

}

// 외부사이트 div Insert--------------------------------------------------
function insert_outlink_div() {
	let info = `외부사이트 이용률을 분석하여 보여드립니다.`;
	let div = 	`
				<div id="anlt_postdata_wrap" class="anlt_visitor_wrap">
					<div class="anlt_visitor_title noselect">외부사이트 분석</div>\
					<div class="anlt_realtime_subtitle noselect">${info}</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">외부사이트 총 클릭수</div>
						<div id="anlt_outlink_click_all_data" class="anlt_visitor_box_data">1,080</div>
					</div>\
					<div class="anlt_visitor_box noselect">
						<div class="anlt_visitor_box_title">외부사이트 최고 클릭수</div>
						<div id="anlt_outlink_click_max_data" class="anlt_visitor_box_data">441</div>
					</div>\
					<div class="anlt_visitor_chart_box">
							<div class="anlt_visitor_box_title_big noselect">외부사이트별 방문수</div>
							<canvas id="anlt_outlink_use_distribution" class="anlt_visitor_chart_element" width="auto" height="auto"></canvas>\
						</div>\
				</div>
	`;
	$("#posts_target").append(div);
	set_outlink_data();
}
function set_outlink_data() {
	get_bar("anlt_outlink_use_distribution",
		['세종대포털', ' 블랙보드', 'UIS', '대양휴머니티칼리지', 'OJ', '두드림', '유드림', '열람실', '도서검색', '북카페', '세종지도', '학사일정', '세종위키'],
		[31, 42, 33, 23, 131, 441, 101, 232, 310, 41, 22, 33, 41]
	);
}

// 디바이스 분석
function insert_device_div() {
	let info = `디바이스별 SOOJLE 이용률을 분석하여 보여드립니다.`;
	let div = 	`
				<div id="anlt_postdata_wrap" class="anlt_visitor_wrap">
					<div class="anlt_visitor_title noselect">디바이스 분석</div>\
					<div class="anlt_realtime_subtitle noselect">${info}</div>\
					<div class="anlt_visitor_chart_box">
						<div class="anlt_visitor_box_title_big noselect">디바이스별 이용률</div>
						<canvas id="anlt_user_device_distribution" class="anlt_visitor_chart_element" width="auto" height="auto"></canvas>\
					</div>\
				</div>
	`;
	$("#posts_target").append(div);
	set_device_data();
}
function set_device_data() {
	$.when(A_JAX(host_ip+"/get_device", "GET", null, null))
	.done(function(data) {
		if (data['result'] == 'success'){
			get_doughnut("anlt_user_device_distribution",
				["PC", "Tablet", "Mobile"],
				[data['pc'], data['tablet'], data['mobile']]
			);
		} 
	});
}



// Chart JS : Line Type---------------------------------------------------**
function get_line(id_, labels_, datas_) {
	let ctx = document.getElementById(id_);
	let myLineChart  = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
			datasets: [{
				label: labels_[0],
				data: datas_[0],
				borderColor: "#03adfc",
				backgroundColor: "#03adfc",
				lineTension: 0,
				fill: false
			}, {
				label: labels_[1],
				data: datas_[1],
				borderColor: "#1ad904",
				backgroundColor: "#1ad904",
				lineTension: 0,
				fill: false
			}]
		},
		options: {
			response: true,
			layout: {
        		padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                },
                labels: {
                	fontSize: 20
                }
        	},
			tooltips: {
				xPadding: 20,
				ypadding: 15,
				titleFontColor: "rgba(0,0,0,0)",
				titleFontSize: 0,
				titleSpacing: 0,
				bodyFontSize: 16,
				bodySpacing: 5,
				mode: 'index',
				intersect: false,
				cornerRadius: 3,
				caretPadding : 20,
				opacity: 0.7,
				footer: ' ',
				footerFontColor: "rgba(0,0,0,0)",
				footerFontSize: 10,
				footerSpacing: 0,
				footerMarginTop: 10
			},
			legend: {
        		display: true,
        		align: 'end'
        	},
        	title: {
        		display: false
        	},
			scales: {
				xAxes: [{
					display: true
				}],
				yAxes: [{
					display: true
				}]
			},
			hover: {
				mode: 'index',
				axis: 'x',
				intersect: false
			}
		}
	});
}
// Chart JS : Bar Type----------------------------------------------------**
function get_bar(id_, date_labels_, labels_, datas_) {
	let ctx = document.getElementById(id_);
	let myBarChart = new Chart(ctx, {
	    type: 'bar',
	    data: {
	    	labels: labels_,
			datasets: [{
				label: date_labels_[1],
				data: datas_[1],
				barPercentage: 0.9,
				categoryPercentage: 0.5,
        		barThickness: 1,
        		maxBarThickness: 2,
        		maxBarThickness: 1,
        		minBarLength: 10,
				backgroundColor: "#1ad904",
			}, {
				label: date_labels_[0],
				data: datas_[0],
				barPercentage: 0.9,
				categoryPercentage: 0.5,
        		barThickness: 1,
        		maxBarThickness: 2,
        		maxBarThickness: 1,
        		minBarLength: 10,
				backgroundColor: "#67a7f2",
			}]
	    },
	    options: {
	    	response: true,
			layout: {
        		padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                },
                labels: {
                	fontSize: 20
                }
        	},
			tooltips: {
				enabled: false
			},
			legend: {
        		display: true,
        		align: 'end'
        	},
        	title: {
        		display: false
        	},
			scales: {
				xAxes: [{
					display: true
				}],
				yAxes: [{
					ticks: {
						min: 0,
						fontSize : 14
					}
				}]
			}
	    }
	});
}
// Chart JS : Doughnut Type-----------------------------------------------**
function get_doughnut(id_, labels_, datas_) {
	let ctx = document.getElementById(id_);
	let myDoughnutChart = new Chart(ctx, {
	    type: 'doughnut',
	    data: {
	    	labels: labels_,
			datasets: [{
				data: datas_,
				backgroundColor: [
									"#007fba",
									"#03adfc",
									"#70cefa" 
								]
			}]
	    },
	    options: {
	    	response: true,
			layout: {
        		padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                },
                labels: {
                	fontSize: 20
                }
        	},
			tooltips: {
				xPadding: 20,
				ypadding: 15,
				titleFontColor: "rgba(0,0,0,0)",
				titleFontSize: 0,
				titleSpacing: 0,
				bodyFontSize: 16,
				bodySpacing: 5,
				mode: 'index',
				intersect: false,
				cornerRadius: 3,
				caretPadding : 20,
				opacity: 0.7,
				footer: ' ',
				footerFontColor: "rgba(0,0,0,0)",
				footerFontSize: 10,
				footerSpacing: 0,
				footerMarginTop: 10
			},
			legend: {
        		display: true,
        		align: 'end'
        	},
        	title: {
        		display: false
        	}
	    }
	});
}

// Dectection User Device 
Detection_Device();
// 방문 날짜 확인
function Check_Visite_Today() {
	let time = localStorage.getItem('sj-visited');
	if (time != null && time != undefined && time != 'undefined') {
		let before = new Date(time);
		before = before.getDate();
		now = new Date().getDate();
		if (now == before) return false;
		else return true;
	} else {
		localStorage.setItem('sj-visited', new Date());
	}
	return true;
}
function Detection_Device() {
	let device = "device_pc";
	if (/(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/.test(navigator.userAgent.toLowerCase()) || (/iPad|iPhone|iPod/.test(navigator.platform) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1))) {
		device = "device_tablet";
	} else if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
	    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
	    device = "device_mobile";
	}
	if (Check_Visite_Today()) {
		A_JAX(host_ip+"/insert_device/"+device, "GET", null, null);
	}
}

let menu_realtime_init = 0;
if (!mobilecheck()) menu_realtime_searchword();
function menu_realtime_searchword() {
	let target = $("#menu_realtime_searchwords_wrapper");
	let target2 = $("#realtime_searchwords_table_words");
	menu_realtime_init = 1;
	target.css("top", "0");
	setTimeout(function() {
		menu_realtime_init = 0;
		$.when(A_JAX(host_ip+"/get_search_realtime", "GET", null, null))
		.done(function (data) {
			if (data['result'] == 'success') {
				target.empty();
				target2.empty();
				let realtime_words_list = data['search_realtime'];
				let div, i;
				if (realtime_words_list.length == 0) {
					div = `<div class="menu_realtime_word noselect">\
							<span>검색이 필요해요!</span>\
						</div>`;
					target.append(div);
				} else {
					for (i = 1; i <= realtime_words_list.length; i++) {
						if (realtime_words_list[i - 1] != undefined) {
							let word = realtime_words_list[i - 1][0];
							div = `<div class="menu_realtime_word noselect">\
										<span style="font-weight:bold; color: #c30e2e">${i}</span>&nbsp;&nbsp;&nbsp;<span>${word}</span>\
									</div>`;
							target.append(div);
						}
					}
					for (i = 1; i <= realtime_words_list.length; i++) {
						if (realtime_words_list[i - 1] != undefined) {
							let word = realtime_words_list[i - 1][0];
							div = `<div class="realtime_searchwords_table_word pointer" onclick="realtime_word_search($(this))">
										<span class="realtime_searchwords_table_num noselect">${i}</span>
										<span class="realtime_searchwords_table_text pointer" onclick="realtime_word_search($(this))">${word}</span>
									</div>`;
							target2.append(div);
						}
					}
				}
			} else {
				div = `<div class="menu_realtime_word noselect"">\
							<span>검색이 필요해요!</span>\
						</div>`;
				target.append(div);
			}
		});
		menu_realtime_moving(0);
	}, 10);
	let day_name = ["일", "월", "화", "수", "목", "금", "토"];
	let time = new Date();
	let year = time.getFullYear();
	let month = time.getMonth() + 1;
	let date = time.getDate();
	let day = time.getDay();
	let hour = addZeros(time.getHours(),2); 
	let minute = addZeros(time.getMinutes(),2);
	let second = addZeros(time.getSeconds(),2);
	let ampm = "AM";
	if (hour > 12) {
		hour -= 12;
		ampm = "PM";
	}
	let now_date = year + '-' + month + '-' + date + " " + day_name[day] + "요일";
	let now_time = hour + ':' + minute + ':' + second;
	let standard = `${now_date} ${ampm} ${now_time} 기준`;
	$("#realtime_searchwords_table_time").append(standard);

}
function menu_realtime_moving(block_h) {
	if (menu_realtime_init == 1) return;
	setTimeout(function() {
		$("#menu_realtime_searchwords_wrapper").css("top", -1 * block_h * 40);
		setTimeout(function() {
			menu_realtime_moving((block_h + 1) % $(".menu_realtime_word ").length);
		}, 500);
	}, 3000);
}


$("#menu_realtime_searchwords").on({
	"mouseenter": function() {	// 메뉴 실시간 검색어 mouseenter
		$("#realtime_searchwords_table").removeClass("display_none");
	}
});
$("#realtime_searchwords_table").on({
	"mouseleave": function() {	// 메뉴 실시간 검색어 mouseleave
		$("#realtime_searchwords_table").addClass("display_none");
	}
});


function number_unit(num, comma = false) {
	if (comma == true) {
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	} else {
		if (num > 1000000) {
			num = Math.round(num/1000000) + 'm';
			return num;
		} else if (num > 1000) {
			num = Math.round(num/1000) + 'k';
			return num;
		} else {
			return num;
		}
	}
}