function search_focus(keyCode) {
	if (keyCode == 13) {
		search_button();
	}
}


function search_button() {	// 검색작업 data = 글자
	let data;
	data = $("#pc_search_input").val();
	$("#pc_search_input").blur();
	search_text(data);	// 검색 함수 실행
	/*search 클릭 작업============================================================*/
}

let is_searching = 0;
function search_text(text) {
	// 현재 검색 중이면 차단
	if (is_searching == 1) return;
	is_searching = 1;

	is_posts_there.a = 0;
	is_posts_done.a = 0;
	if (text == ""){
		Snackbar("검색어를 입력해주세요.");
		return;
	} else {
		text = text.toLowerCase();
	}
	$("#posts_creating_loading").removeClass("display_none");
	$("#posts_target").empty();
	let send_data = {search: text};
	let a_jax_wordanalysis = A_JAX(host_ip+"/simulation_tokenizer", "POST", null, send_data);
	let a_jax_recommend = A_JAX(host_ip+"/get_similarity_words", "POST", null, send_data);
	let a_jax0 = A_JAX(host_ip+"/priority_search/200", "POST", null, send_data);
	$.when(a_jax_wordanalysis).done(function () {
		let json = a_jax_wordanalysis.responseJSON;
		if (json['result'] == 'success') {
			word_tokenizer_display(json["simulation"]);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	})
	$.when(a_jax_recommend).done(function () {
		let json = a_jax_recommend.responseJSON;
		if (json['result'] == 'success') {
			word_similarity_display(json["similarity_words"]);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	});
	$.when(a_jax0).done(function () {
		let json = a_jax0.responseJSON;
		if (json['result'] == 'success') {
			let output = remove_duplicated(0, json["search_result"]);
			insert_search_post(0, output);
			is_posts_done.a += 1;
		} else {
			is_posts_done.a += 1;
			Snackbar("다시 접속해주세요!");
		}
	});
}


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
    return yyyy + "." + (MM[1] ? MM : '0'+ MM[0]) + "." + (dd[1] ? dd : '0'+ dd[0]) + " " +
    		(HH[1] ? HH : '0'+ HH[0]) + ":" + (mm[1] ? mm : '0'+mm[0]) + ":" + (ss[1] ? ss : '0'+ss[0]);
}
var post_tags_search = [];
var post_tags_percent = [];
function insert_search_post(target, posts) {
	post_tags_search.push($("#post1"));
	post_tags_search.push($("#post2"));
	post_tags_search.push($("#post3"));
	post_tags_search.push($("#post4"));
	post_tags_search.push($("#post5"));
	let date1 = new Date(posts[0]["date"]).SetTime(),
		date2 = new Date(posts[1]["date"]).SetTime(),
		date3 = new Date(posts[2]["date"]).SetTime(),
		date4 = new Date(posts[3]["date"]).SetTime(),
		date5 = new Date(posts[4]["date"]).SetTime();
	let dates = [];
	dates.push(date1);
	dates.push(date2);
	dates.push(date3);
	dates.push(date4);
	dates.push(date5);
	posts = posts.slice(0,5);
	let standard = 100/posts[0]["similarity"];
	for (let i = 0; i< 5; i++) {
		post_tags_percent.push(posts[i]["similarity"]);
		let tag = `<div class="view_post_title">${posts[i]["title"]}</div>
						<a href="${posts[i]["url"]}" target="_blank"><div class="view_post_url">${posts[i]["url"]}</div></a>
						<div class="view_post_time">${dates[i]}</div>
						<div class="progress" data-label="${(posts[i]["similarity"]*standard-5).toFixed(3)}%">
						<span class="value" style="width: 0%;"></span>
					</div>`;
		post_tags_search[i].empty();
		post_tags_search[i].append(tag);
	}
	
	for (let i =0; i < 5; i++) {
		post_tags_percent[i] *= standard;
	}
}


let is_posts_done = {
	aInternal: 0,
	aListener: function(val) {},
	set a(val) {
		this.aInternal = val;
		this.aListener(val);
	},
	get a() {
		return this.aInternal;
	},
	registerListener: function(listener) {
		this.aListener = listener;
	}
}
let is_posts_there = {
	aInternal: 0,
	aListener: function(val) {},
	set a(val) {
		this.aInternal = val;
		this.aListener(val);
	},
	get a() {
		return this.aInternal;
	},
	registerListener: function(listener) {
		this.aListener = listener;
	}
}
is_posts_done.registerListener(function(val) {
	if (val == 1) {
		// 로딩 제거
		is_searching = 0;
		moveToinfo(3);
		$("#posts_creating_loading").addClass("display_none");
	}
});
is_posts_there.registerListener(function(val) {
	if (val == 6) {
		$("#posts_creating_loading").addClass("display_none");
		Snackbar("포스트가 존재하지 않습니다.");
	}
});


// Recommend words inserting
function insert_recommend_words(words_dict) {
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
	recommends = recommends.slice(0, 10);
	for (word of recommends) {
		//output.push(Object.keys(word)[0]);
		output.push(word);
	}
	if (output.length == 0) {
		return;
	}
	return output;
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

function word_tokenizer_display(token_array) {
	let target = $("#words_token_cont"), tag;
	target.empty();
	target.append(`<div class="words_token_title noselect">Token 분류</div>`);
	for (let i = 1; i <= token_array.length; i++) {
		if (i == 7) break;
		setTimeout(function() {
			tag = `<div class="words_token noselect wow animated fadeInLeft" data-wow-duration="1s" style="margin-left:${i * 3}vw">${token_array[i - 1]}</div>`;
			target.append(tag);
		}, i*300);
	}
}

let chart_title = [], chart_number = [];
function word_similarity_display(words_array) {
	let output = insert_recommend_words(words_array);
	let target = $("#word_fasttext_cont"), tag;
	target.empty();
	target.append(`<div class="words_token_title noselect">연관 단어 추출</div>`);
	if (output == undefined) return;
	for (let i = 1; i <= output.length; i++) {
		if (i == 7) break;
		setTimeout(function() {
			tag = `<div class="words_fasttext_title noselect wow animated fadeInLeft" data-wow-duration="1s" style="margin-left:${i * 3}vw">${Object.keys(output[i - 1])[0]}</div>`;
			target.append(tag);
		}, i*100);
	}
	for (let i = 0; i < output.length; i ++) {
		if (i == 7) break;
		chart_title.push(Object.keys(output[i])[0]);
		chart_number.push(Object.values(output[i])[0]*100);
	}
	target2 = $("#words__similarity_chart");
	target2.empty().append('<canvas id="hist_bar" width="auto" height="auto"></canvas>');
	// hist(
	// 	"hist_bar", //해당 캔버스 아이디
	// 	chart_title, //레이블
	// 	chart_number,               // 각 레이블의 값
	// );
	target3 = $("#words__vector_chart");
	target3.empty().append('<canvas id="area_vector" width="auto" height="auto"></canvas>');
	//polar_area("area_vector");
}
// Input chart
let target2 = $("#words__similarity_chart"), target3 = $("#words__vector_chart");
// chart js
var myChart1, myChart2;
Chart.defaults.global.defaultFontSize = 20;
Chart.defaults.global.defaultFontColor = 'white';
Chart.defaults.global.defaultFontFamily = "'AppleSdNeo'";
function hist(id_, labels_, data_) {
    var ctx = document.getElementById(id_);
    myChart1 = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels_,
            datasets: [{
                label: ' ',
                data: data_,
                backgroundColor: "rgba(255,255,255,0.2)",
                borderColor: "white",
                borderWidth: 3,
                barThickness: 30,
                minBarLength: 50
            }]
        },
        options:{
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
        		titleFontSize: 24,
        		bodyFontSize: 20
        	},
        	legend: {
        		display: false
        	},
        	title: {
        		display: false
        	},
        	scales: {
        		yAxes: [{
        			fontSize: 20,
        			fontColor: "white",
        			barThickness: 30
        		}],
        		xAxes: [{
        			fontSize: 20,
        			fontColor: "white",
        			barThickness: 30
        		}]
        	},
        	animation: {
				duration: 2000
			}
        }
    });
}
var randomScalingFactor = function() {
	return Math.random() * 100;
};
function polar_area(id_) {
	var ctx2 = document.getElementById(id_);
	myChart2 = new Chart(ctx2, {
		type: "polarArea",
		data: {
			datasets: [{
				label: ' ',
				data: [
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
				],
				backgroundColor: [
					'#ed0202',
					'#ff6600',
					'#ffd000',
					'#a6ff00',
					'#00ffaa',
					'#00f2ff',
					'#0051ff',
					'#5900ff',
					'#c300ff',
					'#ff00c8',
					'#ed0202',
					'#ff6600',
					'#ffd000',
					'#a6ff00',
					'#00ffaa',
					'#00f2ff',
					'#0051ff',
					'#5900ff',
					'#c300ff',
					'#ff00c8',
					'#ed0202',
					'#ff6600',
					'#ffd000',
					'#a6ff00',
					'#00ffaa',
					'#00f2ff',
					'#0051ff',
					'#5900ff',
					'#c300ff',
					'#ff00c8'
				],
				borderColor: 'rgba(0,0,0,1)'
			}],
			labels: [
				'v1',
				'v2',
				'v3',
				'v4',
				'v5',
				'v6',
				'v7',
				'v8',
				'v9',
				'v10',
				'v11',
				'v12',
				'v13',
				'v14',
				'v15',
				'v16',
				'v17',
				'v18',
				'v19',
				'v20',
				'v21',
				'v22',
				'v23',
				'v24',
				'v25',
				'v26',
				'v27',
				'v28',
				'v29',
				'v30',
			]
		},
		options: {
			responsive: true,
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
        		titleFontSize: 24,
        		bodyFontSize: 20
        	},
        	legend: {
        		position: 'left'
        	},
        	title: {
        		display: false
        	},
        	scale: {
				ticks: {
					beginAtZero: true,
					backdropColor: 'rgba(0,0,0,0)',
					showLabelBackdrop: true
				},
				reverse: false
			},
			animation: {
				animateRotate: false,
				animateScale: true,
				duration: 2000
			}
		}
	});
}


function moveToinfo(num) {
	let target_offset = $(`div.content__section:nth-child(${num})`).offset().top;
	$('html,body').animate({scrollTop: target_offset}, 1000);
}

function page_reload() {
	$('html, body').animate({
		scrollTop: 0
	}, 1000);
	setTimeout(function() {
		location.reload();
	}, 1000);
}
