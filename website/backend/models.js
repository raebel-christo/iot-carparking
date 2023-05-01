const { ObjectId } = require('mongodb');
const mongoose = require('mongoose');

const User = new mongoose.Schema({
    // id: {type: ObjectId, required: true},
    slot: {type: Number, required: true},
    // id: {type: Number, required: true},
    plate : {type: String, required: true},
    in_time : {type: Date},
})

 const Car = mongoose.model('cars',User);

 module.exports = Car;