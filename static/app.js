$(document).ready(function(){
    $("#toggle-menu").click(function(){
        $(".side-menu").toggleClass("menu-open");
    });

    $("#save-button").click(function(){
        $.ajax({
            type: 'POST',
            url: '/save_contract',
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                alert(response.message);
            }
        });
    });
    $(".dropdown-item").click(function() {
        var selectedRating = $(this).data("rating");
        $.ajax({
            type: 'POST',
            url: '/feedback',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'rating': selectedRating}),
            success: function(response) {
                alert(response.message);
            }
        });
    });

    $("#send-button").click(function(){
        var user_input = $("#user-input").val();
        $("#user-input").val("");


        $.ajax({
            type: 'POST',
            url: '/send_message',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'user_input': user_input}),
            success: function(response) {
                $("#chat-output").append('<div class="message-container user-message"><div class="message">' + response.user_message + '</div></div>');
                $("#chat-output").append('<div class="message-container system-message"><div class="message"><pre>' + response.system_message + '</pre></div></div>');
                var container = $("#chat-output");
                if (response.system_message!='We only generate contracts related to the real estate domain.'){
                    $("#chat-output").append('<div class="message-container system-message"><div class="message"><pre>Please Provide any editing preferences you might have. If you are satisfied, you can click the save button.</pre></div></div>');
                }
                container.scrollTop(container[0].scrollHeight);
            }
        });
    });
});