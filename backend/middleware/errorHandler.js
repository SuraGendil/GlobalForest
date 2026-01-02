const constants = require('../constants');

const errorHandler = (err, req, res, next) => {
    const statusCode = res.statusCode ? res.statusCode : 500;
    console.log(statusCode);

    let errorTitle = "";
    switch (statusCode) {
        case constants.constants.VALIDATION_ERROR:
            errorTitle = "Validation Error";
            break;
        case constants.constants.UNAUDTHORIZED:
            errorTitle = "Unauthorized";
            break;
        case constants.constants.FORBIDDEN:
            errorTitle = "Forbidden";
            break;
        case constants.constants.NOT_FOUND:
            errorTitle = "Not Found";
            break;
        case constants.constants.SERVER_ERROR:
            errorTitle = "Server Error";
            break;
        default:
            errorTitle = "Unknown Error";
            break;
    }

    res.status(statusCode).json({
        message: err.message,
        title: errorTitle,
        stackTrace: err.stack
    });
}

module.exports = {errorHandler};