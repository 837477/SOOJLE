// Recommend posts for these users.
const USER_ID = ['16011075', '16011089', '16011092'];
const USER_TOKEN = [
	null, null, null
]

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
function polar_area(id_, data_) {
	var ctx2 = document.getElementById(id_);
	let len = data_.length;
	myChart2 = new Chart(ctx2, {
		type: "polarArea",
		data: {
			datasets: [{
				label: ' ',
				data: data_,
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
				].slice(0, len),
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
			].slice(0, len)
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
        		display: false
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
let lda_list, fasttext_list;
recommend();
function recommend() {
	let index = Math.round(Math.random() * (USER_ID.length - 1));
	let user_id = USER_ID[index];
	let a_jax = A_JAX(host_ip+"/simulation_get_user_measurement/" + user_id, "GET", null, null);
	$.when(a_jax).done(function () {
		let json = a_jax.responseJSON;
		if (json['result'] == 'success') {
			setTimeout(function() {
				$("#user_lda_cont").append(`<canvas id="user_lda_content" class="chart_plus" width="auto" height="auto"></canvas>`);
				$("#user_fasttext_cont").append(`<canvas id="user_fasttext_content" class="chart_plus" width="auto" height="auto"></canvas>`);
				lda_list = json['user']['topic'];
				recommend_lda_chart(json['user']['topic']);
				fasttext_list = json['user']['ft_vector'];
				recommend_fasttext_chart(json['user']['ft_vector']);
				recommend_tag_chart(json['user']['tag']);
			}, 500);
			$("#recommend_analysis_element_introduce").text(`${json['user']['user_id']} ${json['user']['user_name']}`);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	});
	let a_jax_token = A_JAX_TOKEN(host_ip+"/get_recommendation_newsfeed", "GET", USER_TOKEN[index], null);
	$.when(a_jax_token).done(function () {
		let json = a_jax_token.responseJSON;
		if (json['result'] == 'success') {
			let output = JSON.parse(json["newsfeed"]);
			output = output.slice(0, 6);
			creating_post(output);
		} else {
			Snackbar("다시 접속해주세요!");
		}
	});
}
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
function creating_post(posts) {
	let post_tags_search = [];
	post_tags_search.push($("#post1"));
	post_tags_search.push($("#post2"));
	post_tags_search.push($("#post3"));
	post_tags_search.push($("#post4"));
	post_tags_search.push($("#post5"));
	post_tags_search.push($("#post6"));
	let date1 = new Date(posts[0]["date"].$date).SetTime(),
		date2 = new Date(posts[1]["date"].$date).SetTime(),
		date3 = new Date(posts[2]["date"].$date).SetTime(),
		date4 = new Date(posts[3]["date"].$date).SetTime(),
		date5 = new Date(posts[4]["date"].$date).SetTime(),
		date6 = new Date(posts[5]["date"].$date).SetTime();
	let dates = [];
	dates.push(date1);
	dates.push(date2);
	dates.push(date3);
	dates.push(date4);
	dates.push(date5);
	dates.push(date6);
	for (let i = 0; i< 6; i++) {
		let tag = `<div class="view_post_title">${posts[i]["title"]}</div>
						<a href="${posts[i]["url"]}" target="_blank"><div class="view_post_url">${posts[i]["url"]}</div></a>
						<div class="view_post_time">${dates[i]}</div>
					</div>`;
		post_tags_search[i].empty();
		post_tags_search[i].append(tag);
	}
}

function recommend_lda_chart(lda) {
	polar_area('user_lda_content', lda);
}
function recommend_fasttext_chart(fasttext) {
	polar_area('user_fasttext_content', fasttext);
}
function recommend_tag_chart(tags) {
	let output = [];
	let tag, tag_value;
	for (tag in tags) {
		tag_value = tags[tag];
		let dict = {};
		dict[tag] = tag_value;
		output.push(dict);
	}
	output.sort(function(a, b) {
    	return Object.values(b)[0] - Object.values(a)[0];
	});
	output = output.slice(0, 5);
	let target = $("#user_tag_cont"), tag_form;
	for (let i = 0; i < 5; i++) {
		tag_form = `<div class="user_element_tag noselect">${Object.keys(output[i])[0]}</div>`
		target.append(tag_form);
	}
}

function page_reload() {
	$('html, body').animate({
		scrollTop: 0
	}, 1000);
	setTimeout(function() {
		location.reload();
	}, 1000);
}

// static token ajax
function A_JAX_TOKEN(url, type, token, data){
    let authorization;
    if (token != null && token != undefined && token != 'undefined') {
        authorization = {'Authorization': "Bearer " + token};
    } else {
        authorization = {};
    }
    let ajax_;
    ajax_ = $.ajax({
        headers: authorization,
        type: type,
        url: url,
        data: data,
        dataType : "json",
        success: function(res){
        },
        error: function(res){
        }
    });
    return ajax_;
}

