document.addEventListener('DOMContentLoaded', () => {

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
        socket.emit('joined');

        document.querySelector('#new-channel').onclick = () => {
            localStorage.removeItem('last_channel');
        };

        document.querySelector('#leave-channel').onclick = () => {
            socket.emit('left');
            localStorage.removeItem('last_channel');
            window.location.replace('/create_channel');
        };

        document.querySelector('#logout').onclick = () => {
            localStorage.removeItem('last_channel');
            localStorage.clear();
        };

        document.querySelector('#message-textbox').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });
        
        document.querySelector('#send-button').onclick = () => {
            
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();
            let msg = document.getElementById("message-textbox").value;
            socket.emit('send message', msg, timestamp);

            document.getElementById("message-textbox").value = '';
        };
  });
  
  socket.on('status', data => {
      const p = document.createElement('p');
      p.innerHTML = data.msg;
      document.querySelector('#chat').append(p)

      localStorage.setItem('last_channel', data.channel)
  })

  socket.on('show message', data => {
      const p = document.createElement('p');
      p.innerHTML = `${data.timestamp}` + ' - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`;
      document.querySelector('#chat').append(p);
  })
});
