const Case = require('../models/Case');
const asyncHandler = require('express-async-handler');

//  @desc Geat all case
//  @route GET /api/case
//  @access Public

const getCases = asyncHandler(async(req, res) => {
    const cases = await Case.find();
    res.status(200).json(cases);

    // res.status(200).json({ message: 'Get all case' });
});

//  @desc Create new case
//  @route POST /api/case
//  @access Public

const createCase = asyncHandler(async(req, res) => {
    const {country, driver, year, loss} = req.body;
    if (!country || !driver || !year || !loss) {
        res.status(400);
        throw new Error('Missing required fields');
    }
    const newcase = await Case.create({
        country,
        driver,
        year,
        loss
    });
    res.status(201).json(newcase);
});

//  @desc Get single case
//  @route GET /api/case/:id
//  @access Public

const getCase = asyncHandler(async(req, res) => {
    const cases = await Case.findById(req.params.id);
    if (!cases) {
        res.status(404);
        throw new Error('Case not found');
    }
    res.status(200).json(cases);
});

//  @desc Update case
//  @route PUT /api/case/:id
//  @access Public

const updateCase = asyncHandler(async(req, res) => {
    const cases = await Case.findById(req.params.id);
    if (!cases) {
        res.status(404);
        throw new Error('Case not found');
    }
    const updatedCase = await Case.findByIdAndUpdate(
        req.params.id, 
        req.body, 
        { new: true });
    res.status(200).json(updatedCase);
});

//  @desc Delete case
//  @route DELETE /api/case/:id
//  @access Public

const deleteCase = asyncHandler(async(req, res) => {
    const cases = await Case.findById(req.params.id);
    if (!cases) {
        res.status(404);
        throw new Error('Case not found');
    }
    await Case.deleteOne({ _id: req.params.id });
    res.status(200).json({ message: `Delete case for ${req.params.id}` });
});


module.exports = {
    getCases,
    createCase,
    getCase,
    updateCase,
    deleteCase
};