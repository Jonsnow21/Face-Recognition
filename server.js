let redis = require('redis');
let express = require('express');

let app = express();
let pub = redis.createClient();
let sub = redis.createClient();

app.get('/', (req, res) => {
	pub.publish('test', 'images/rneeraj1.jpg');

	sub.subscribe('result')

	sub.on('message', function(channel, message) {
        console.log("sub channel " + channel + ": " + message);

        sub.unsubscribe();
        sub.quit();
        pub.quit();

        if (message === 'ERR_NOT_FOUND_IN_DB') {
            res.status(404).json({
                error: 'ERR_NOT_FOUND_IN_DB'
            })
        } else {
            res.status(200).json({
                "Name": message.split('|')[0],
                "Phone": message.split('|')[1]
            })
        }

	})
});

app.listen(3000, () => 
	console.log('Example app listening on port 3000!'))
