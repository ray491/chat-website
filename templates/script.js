$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            data : {
                user_input : $('#user_input').val()
            },
            type : 'POST',
            url : '/chatbot'
        })
        .done(function(data) {
            $('#chat-area').append("<p>" + data + "</p>");
            $('#user_input').val('');
        });
    });
});