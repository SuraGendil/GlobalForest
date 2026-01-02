const mongoose = require('mongoose');

const caseSchema = new mongoose.Schema({
    country:{
        type: String,
        required: [true, 'Please add a country']
    },
    driver:{
        type: String,
        required: [true, 'Please add a driver']
    },
    year:{
        type: Number,
        required: [true, 'Please add a year']
    },
    loss:{
        type: Number,
        required: [true, 'Please add a loss']
    }
}, {
    timestamps: true
});

module.exports = mongoose.model('Case', caseSchema);