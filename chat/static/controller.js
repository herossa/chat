$(document).ready(function() {
    var post_url = location.protocol + '//' + document.domain + ':' + location.port + '/new_message/';
    var get_url = location.protocol + '//' + document.domain + ':' + location.port + '/' + page_data['room'] + '/get_messages/';

    var namespace = '/alert';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('update_list', function(msg) {
        if (msg['data'] == page_data['room']) {
            makeGet(get_url);
        }
    });

    function makePost(url, data) {
        var request = {
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            tradicional: true,
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
            }
        }
        $.ajax(request);
    }

    function makeGet(url) {
        var request = {
            type: 'GET',
            url: url,
            contentType: "application/json; charset=utf-8",
            tradicional: true,
            success: function(response) {
                if (response['result'] != undefined) {
                    $("#list-message").empty();
                    for (var i = response['result'].length - 1; i >= 0; i--) {
                        insertItemList(response['result'][i]);
                        scrollBotton();
                    }
                }
            },
            error: function(error) {
            }
        }
        $.ajax(request);
    }

    function insertItemList(item) {
        $("#list-message").append('<li>' + item['user'] + " says("+item['date_time']+"): "+item["message"] + '</li>')
    }

    $('form#message').submit(function(e) {
        if ($('#message_data').val() != "") {
            var post_data = {
                'message': {
                    'user': page_data['user'],
                    'room': page_data['room'],
                    'message': $('#message_data').val(),
                    'date_time': new Date(new Date().getTime()).toLocaleString()
                }
            };
            makePost(post_url, post_data);
            socket.emit('new_message', {data: page_data['room']});
            document.getElementById('message_data').value = "";
        }
        return false;
    });

    function scrollBotton(){
       var div = document.getElementById('app-messages');
       div.scrollTop = div.scrollHeight - div.clientHeight;
    }

    setTimeout(makeGet(get_url), 1);
});