$(function () {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/match/" + match_id;
    var socket = new ReconnectingWebSocket(ws_path);

    $('.upgrade-control').click(function () {
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
    $('.stat-control').change(function () {
        var data = $(this).attr("id").split("-");
        var message = {
            type: "stat",
            field: data[0],
            id: data[1],
            value: $(this).val()
        };
        socket.send(JSON.stringify(message));
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
            $('#'+data.field+'-'+data.id).val(data.value);
        }
    };

});