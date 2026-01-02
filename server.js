const express = require('express');
const dotenv = require('dotenv').config();
const { connect } = require('mongoose');
const { errorHandler } = require('./middleware/errorHandler');
const connectDB = require('./connection/dbConnection');

connectDB();
const app = express();

app.use(express.json());
app.use("/api/case", require("./routes/caseRoutes"));
app.use(errorHandler);
const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
})