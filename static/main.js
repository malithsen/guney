$(function() {
    $('button').click(function(e) {
        e.preventDefault();
        var text = $('#chatbox').val();
        $('#messages').append('<li>You: '+text+'</li>');
        $('#chatbox').val('');
        $.ajax({
            type: "POST",
            url: "/chat",
            data: JSON.stringify({"text":text}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (msg) {
               $('#messages').append('<li>'+msg.response+'</li>');
            },
            error: function (errormessage) {
                console.log(errormessage);

            }
        });
    });
});