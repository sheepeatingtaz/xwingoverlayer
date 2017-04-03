$(document).ready(function () {
    $('.marquee').marquee();
    $('.image-marquee').marquee({
        duration: 15000,
        duplicated: true
    });
    $("#timer").countdown(finish_time, function (event) {
        $(this).html(
            '<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_1_icon + '"></i>&nbsp;' + event.strftime('%H:%M:%S') + '&nbsp;<i class="shrunken xwing-miniatures-font xwing-miniatures-font-' + player_2_icon + '"></i>'
        );
    });
});