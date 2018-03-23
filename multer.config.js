let multer = require('multer');

const getExtension = (name)=>{
    let local = name.split('.');

    return local[local.length - 1]
}

const storage = multer.diskStorage({
	destination: function (req, file, cb) {
		if (!file) {
			return;
		}
		cb(null, 'images/');
	},
	filename: function (req, file, cb) {
		if (!file) {
			return;
		}
		cb(null, file.originalname)
	}
});

module.exports = multer({ storage });