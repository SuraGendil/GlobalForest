const express = require('express');
const router = express.Router();
const {getCases, createCase, getCase, updateCase, deleteCase} = require('../JS/controllers/caseController');

router.route("/").get(getCases);

router.route("/").post(createCase);

router.route("/:id").get(getCase);

router.route("/:id").put(updateCase);

router.route("/:id").delete(deleteCase);

module.exports = router;