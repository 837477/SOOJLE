function A_JAX(url, type, nope, data){
    let token = sessionStorage.getItem('sj-state');
    let authorization;
    if (token != null && token != undefined && token != 'undefined') {
        authorization = {'Authorization': "Bearer " + token};
    } else {
        authorization = {};
    }
    let ajax_ = $.ajax({
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

function A_JAX_FILE(url, type, nope, data){
    let token = sessionStorage.getItem('sj-state');
    let authorization;
    if (token != null && token != undefined && token != 'undefined') {
        authorization = {'Authorization': "Bearer " + token};
    } else {
        authorization = {};
    }
    let ajax_ = $.ajax({
        headers: authorization,
        type: type,
        url: url,
        data: data,
        dataType : "json",
        processData : false,
        contentType : false,
        success: function(res){
        },
        error: function(res){
        }
    });
    return ajax_;
}

function A_JAX_CORS(url, type){
    let ajax_ = $.ajax({
        crossOrigin : true,
        type: type,
        url: url,
        dataType : "json",
        success: function(res){
        },
        error: function(res){
        }
    });
    return ajax_;
}