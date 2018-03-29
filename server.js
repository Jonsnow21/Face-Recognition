let redis = require('redis');
let express = require('express');
let bodyParser = require('body-parser');
let upload = require('./multer.config.js');

let app = express();
let pub = redis.createClient();
let sub = redis.createClient();

app.use(bodyParser.urlencoded({
    extended: false
}));

app.use(bodyParser.json());

app.post('/',  upload.array('file', 10), (req, res) => {

    console.log(req.body)

    sub.subscribe('result')

    if (req.body.type === 'init') {
        console.log(req.body)
        res.status(200).json({
            "message": "init"
        })
        sub.unsubscribe()
        return;
    }

    if (req.body.type === 'test')
        pub.publish(req.body.type, req.body.data);
	else
	    pub.publish(req.body.type, JSON.stringify(req.body.data));


	let count = 0;

	const subScribe = ()=>{
	    return new Promise((resolve, reject)=>{
	        sub.on('message', function(channel, message) {

                console.log("sub channel " + channel + ": " + message, count++);

                if (message === 'PERSON_NOT_FOUND_IN_DB') {
                    resolve(0)
                } else if(message === 'SUCCESS') {
                    resolve(1)
                } else {
                    resolve(message)
                }

            })
	    })
	}

	return Promise.resolve().then(subScribe).then((data)=>{
	    sub.unsubscribe();

	    if(data === 0){
	        res.status(404).json({message: 'Not found'})
	    } else if(data === 1){
	        res.status(200).json({message: 'Success'})
	    } else {
	        res.status(200).json({
                "Name": data
            })
	    }
	})


});

app.listen(3000, () => 
	console.log('Example app listening on port 3000!'))
