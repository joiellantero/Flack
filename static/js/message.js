document.addEventListener('DOMContentLoaded', () => {

    var alert_socket = io('http://127.0.0.1:5000/alert');

    document.querySelector('#send-username').onclick = () => {
        alert_socket.emit('username', document.querySelector('#sender').innerHTML)
    };

    document.querySelector('#send-alert-message').onclick = () => {
        var recipient = document.querySelector('#recipient').innerHTML;
        var message_to_send = document.querySelector('#alert-message').value;

        alert_socket.emit('alert_message', {'username': recipient, 'message': message_to_send});
    };

    alert_socket.on('new_alert_message', function(msg){
        alert(msg);
    });
});