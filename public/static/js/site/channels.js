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

    socket.onmessage = function (message) {
        var data = JSON.parse(message.data);
        if (data.type == "upgrade") {
            $('#upgrade-' + data.id + "-" + data.pilot_id).prop('checked', data.value);
            $('#upgrades-' + data.pilot_id).html(data.upgrades);
            $('#upgrades-' + data.pilot_id).marquee();
        }
        if (data.type == "stat") {
            $('#'+data.field+'-'+data.id).text(data.value);
            $('#'+data.field+'-'+data.id+'-up').attr('data-value', parseInt(data.value)+1);
            $('#'+data.field+'-'+data.id+'-down').attr('data-value', parseInt(data.value)-1);
            // $('#'+data.field+'-'+data.id).val(data.value);
        }
        if (data.type == "start_clock") {
            console.log(data)
            var finish_time = data.finish_time;
            $("#timer").countdown(finish_time, function (event) {
            $(this).html(
                '<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_1_icon + '"></i>&nbsp;' + event.strftime('%H:%M:%S') + '&nbsp;<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_2_icon + '"></i>'
            );
        });
        }
    };

});