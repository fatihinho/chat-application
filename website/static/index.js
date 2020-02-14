/*
 * Statik dosyayı çağırabilmek için browser'daki ön belleği temizleyerek sayfayı yenilemek gerekir.
 */

$(function() {
    $('#sendBtn').bind('click', function() {
        var value = document.getElementById("msg").value;
        console.log(value);
        document.getElementById("msg-text").innerHTML = value;
        $.getJSON('/send_message',
            {val: value}, // val parametresi ile değerimizi back-end'e taşıyoruz
            function(data) {

            });
        fetch('/get_messages')
            .then(function (response) {
                return response.text();
            }).then(function (text) {
                console.log('GET response text:');
                console.log(text); // Print the greeting as text
            });
        return false;
    });
});

function validate(name) {
    if (name.length >= 2) {
        return true;
    }
    return false;
}