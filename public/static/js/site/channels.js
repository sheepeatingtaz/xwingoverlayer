$(function () {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/match/" + match_id;
    var socket = new ReconnectingWebSocket(ws_path);

    $('.upgrade-control').change(function () {
        var data = $(this).attr("id").replace(/upgrade-/gi, '').split("-");
        var message = {
            type: "upgrade",
            id: data[0],
            pilot_id: data[1],
            value: $(this).is(":checked")
        };
        socket.send(JSON.stringify(message));
        return false;
    });
    $('.stat-control').click(function () {

        var data = $(this).attr("id").split("-");
        var message = {
            type: "stat",
            field: data[0],
            id: data[1],
            value: $(this).attr("data-value")
        };
        socket.send(JSON.stringify(message));
        return false;
    });
    $('.start-match').click(function () {
        var data = $(this).attr("id").split("-");
        var message = {
            type: "start_clock",
            id: data[2]
        };
        socket.send(JSON.stringify(message));
        return false;
    });
    $('.show-image').click(function () {
        var url = $(this).attr("data-image-url");
        var message = {
            type: "image",
            value: url
        };
        console.log(url);
        socket.send(JSON.stringify(message));
        return false;
    });
    $('.please_wait').click(function () {
        var data = $(this).attr("id").split("-");
        var message = {
            type: "please_wait",
            value: data[2]
        };
        socket.send(JSON.stringify(message));
        return false;
    });


    socket.onmessage = function (message) {
        var data = JSON.parse(message.data);
        if (data.type == "upgrade") {
            $('#upgrade-' + data.id + "-" + data.pilot_id).prop('checked', data.value);
            $('#upgrades-' + data.pilot_id).html(data.upgrades);
            $('#upgrades-' + data.pilot_id).marquee();
        }
        if (data.type == "stat") {
            $('#' + data.field + '-' + data.id).text(data.value);
            $('#' + data.field + '-' + data.id + '-up').attr('data-value', parseInt(data.value) + 1);
            $('#' + data.field + '-' + data.id + '-down').attr('data-value', parseInt(data.value) - 1);
            if(data.field=="hull" && data.value <= 0){
                $('#pilot-' + data.id).addClass("destroyed")
            }
        }

        if (data.type == "image") {
            var image_href = data.value;
            if (image_href) {
                if ($('#lightbox').length > 0) { // #lightbox exists
                    //place href as img src value
                    $('#content').html('<img src="' + static_url + image_href + '" />');
                    //show lightbox window - you could use .show('fast') for a transition
                    $('#lightbox').show('fast');
                } else {
                    var lightbox =
                        '<div id="lightbox">' +
                        '<div id="content">' + //insert clicked link's href into img src
                        '<img src="' + static_url + image_href + '" />' +
                        '</div>' +
                        '</div>';

                    //insert lightbox HTML into page
                    $('body').append(lightbox);
                }
                setTimeout(function () {
                    $('#lightbox').hide('fast');
                }, 7000);
            }
        }
        if (data.type == "start_clock") {
            var finish_time = data.finish_time;
            $("#timer").countdown(finish_time, function (event) {
                $(this).html(
                    '<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_1_icon + '"></i>&nbsp;' + event.strftime('%H:%M:%S') + '&nbsp;<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_2_icon + '"></i>'
                );
            });
        }

        if (data.type == "please_wait") {
            $(".please-wait").toggle();
        }
    };

});
