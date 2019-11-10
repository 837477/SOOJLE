function A_JAX(url, type, token, data){
    var ajax_;
    ajax_ = $.ajax({
        type: type,
        url: url,
        data: data,
        headers: {"Authorization": 'Bearer ' + token },
        dataType : "json",
        success: function(res){
            
        },
        error: function(res){
            
        }
    });
    return ajax_;
}

function newsfeed() {
    
    $("#test_newsfeed").empty();
    var newsfeed_list = A_JAX("http://192.168.0.21:5000/get_recommendation_newsfeed", "GET", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzMwMzgzNzMsIm5iZiI6MTU3MzAzODM3MywianRpIjoiYWFmNTQ3MDQtYzdkYS00MTcwLWI1NmYtOTI4YWNhZTJlZmRjIiwiaWRlbnRpdHkiOiJ0ZXN0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.yDwdkgx_-ab_G-u0ko_UkOkijEiDxdyfDMEMrlBeOks", null);
        $.when(newsfeed_list).done(function () {

           if (newsfeed_list.responseJSON['result'] == 'success') {
                
                newsfeed = newsfeed_list.responseJSON['newsfeed'];

                console.log(newsfeed);

                //for(let i=0; i<newsfeed.length; i++) 
                for (let i in newsfeed){
                    output = `<p>#######################################<br>${newsfeed[i]['title']}<br>ID = ${newsfeed[i]["_id"]}<br>TOS = ${newsfeed[i]["TOS"]}<br>TAS = ${newsfeed[i]["TAS"]}<br>FAS = ${newsfeed[i]["FAS"]}<br>RANDOM = ${newsfeed[i]["RANDOM"]}<br>TOTAL = ${newsfeed[i]["similarity"]}<br>#######################################<br><br></p>`;
                    console.log(output);
                    $("#test_newsfeed").append(output);
                }


           }
        });
    
}

function search_() {
    $("#test_newsfeed").empty();
    var saerch_text = $("#search_box").val();
    
     var newsfeed_list1 = A_JAX("http://192.168.0.21:5000/search_title", "POST", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzMwMzgzNzMsIm5iZiI6MTU3MzAzODM3MywianRpIjoiYWFmNTQ3MDQtYzdkYS00MTcwLWI1NmYtOTI4YWNhZTJlZmRjIiwiaWRlbnRpdHkiOiJ0ZXN0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.yDwdkgx_-ab_G-u0ko_UkOkijEiDxdyfDMEMrlBeOks", {'search': saerch_text});
        $.when(newsfeed_list1).done(function () {

           if (newsfeed_list1.responseJSON['result'] == 'success') {
                console.log(newsfeed_list1);

                search_result = newsfeed_list1.responseJSON['search_result'];

                for (let i in search_result){
                    output = `<p>${search_result[i]['title']} </p>`;
                    $("#test_newsfeed").append(output);
                }

            $("#test_newsfeed").append("<p>===========================================================</p>");
           }
           
        });

    

     var newsfeed_list2 = A_JAX("http://192.168.0.21:5000/search_token", "POST", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzMwMzgzNzMsIm5iZiI6MTU3MzAzODM3MywianRpIjoiYWFmNTQ3MDQtYzdkYS00MTcwLWI1NmYtOTI4YWNhZTJlZmRjIiwiaWRlbnRpdHkiOiJ0ZXN0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.yDwdkgx_-ab_G-u0ko_UkOkijEiDxdyfDMEMrlBeOks", {'search': saerch_text});
        $.when(newsfeed_list2).done(function () {

           if (newsfeed_list2.responseJSON['result'] == 'success') {
                console.log(newsfeed_list2);

                search_result = newsfeed_list2.responseJSON['search_result'];

                for (let i in search_result){
                    output = `<p>${search_result[i]['title']} </p>`;
                    $("#test_newsfeed").append(output);
                }

                $("#test_newsfeed").append("<p>===========================================================</p>");
           }

        });


     var newsfeed_list3 = A_JAX("http://192.168.0.21:5000/search_ft_token", "POST", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzMwMzgzNzMsIm5iZiI6MTU3MzAzODM3MywianRpIjoiYWFmNTQ3MDQtYzdkYS00MTcwLWI1NmYtOTI4YWNhZTJlZmRjIiwiaWRlbnRpdHkiOiJ0ZXN0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.yDwdkgx_-ab_G-u0ko_UkOkijEiDxdyfDMEMrlBeOks", {'search': saerch_text});
        $.when(newsfeed_list3).done(function () {

           if (newsfeed_list3.responseJSON['result'] == 'success') {
                console.log(newsfeed_list3);

                search_result = newsfeed_list3.responseJSON['search_result'];

                for (let i in search_result){
                    output = `<p>${search_result[i]['title']} :::  </p>`;
                    $("#test_newsfeed").append(output);
                }


           }
        });
}

function refresh_() {
    alert('관심도 갱신작업이 시작되었습니다. 다소 시간이 걸릴 수 있습니다. 2~3분 이내');

    var LDA_BOX = $("#LDA_box").val();
    var FT_BOX = $("#FT_box").val();

    var refresh_ = A_JAX("http://192.168.0.21:5000/refresh_measurement", "POST", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzMwMzgzNzMsIm5iZiI6MTU3MzAzODM3MywianRpIjoiYWFmNTQ3MDQtYzdkYS00MTcwLWI1NmYtOTI4YWNhZTJlZmRjIiwiaWRlbnRpdHkiOiJ0ZXN0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.yDwdkgx_-ab_G-u0ko_UkOkijEiDxdyfDMEMrlBeOks", {"LDA": LDA_BOX, "FAST": FT_BOX});
        $.when(refresh_).done(function () {

           if (refresh_.responseJSON['result'] == 'success') {
                
                alert('관심도가 갱신되었습니다. 페이지를 새로고침 해주세요.');
           }
        });
}

