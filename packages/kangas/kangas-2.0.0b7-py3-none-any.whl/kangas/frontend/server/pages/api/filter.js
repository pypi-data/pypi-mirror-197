"use strict";
(() => {
var exports = {};
exports.id = 357;
exports.ids = [357];
exports.modules = {

/***/ 22798:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Z": () => (/* binding */ config)
});

;// CONCATENATED MODULE: external "process"
const external_process_namespaceObject = require("process");
;// CONCATENATED MODULE: ./config.js

const localConfig = {
    apiUrl: `${external_process_namespaceObject.env.KANGAS_PROTOCOL || "http"}://${external_process_namespaceObject.env.KANGAS_HOST}:${external_process_namespaceObject.env.KANGAS_BACKEND_PORT}/datagrid/`,
    rootUrl: `${external_process_namespaceObject.env.KANGAS_PROTOCOL || "http"}://${external_process_namespaceObject.env.KANGAS_HOST}:${external_process_namespaceObject.env.PORT}/`,
    defaultDecimalPrecision: 5,
    locale: "en-US",
    hideSelector: external_process_namespaceObject.env.KANGAS_HIDE_SELECTOR === "1",
    cache: true,
    prefetch: false,
    debug: false
};
/* harmony default export */ const config = (localConfig);


/***/ }),

/***/ 63332:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22798);

const handler = async (req, res)=>{
    const query = new URLSearchParams(req.query);
    const result = await fetch(`${_config__WEBPACK_IMPORTED_MODULE_0__/* ["default"].apiUrl */ .Z.apiUrl}verify-where?dgid=${query?.get("dgid")}&timestamp=${query?.get("timestamp")}&whereExpr=${query?.get("where")}`, {
        next: {
            revalidate: 1440
        }
    });
    const json = await result.json();
    res.send(json);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (handler);


/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__(63332));
module.exports = __webpack_exports__;

})();