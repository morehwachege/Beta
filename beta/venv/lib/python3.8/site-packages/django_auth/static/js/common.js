/*
* set global delimiters in Vue.js 2.0
*/
Vue.options.delimiters = ['[[', ']]'];
Vue.config.productionTip = false;

window.canRequest = new Array();

/***
 * Send http POST request and get response data
 * @param url
 * @param method
 * @param param
 * @param callback
 * @private
 */
function _dqRequest(url, method, param, callback) {

    if (window.canRequest[callback] == undefined || window.canRequest[callback]) {
        window.canRequest[callback] = false;
        window.deviceClientWidth = document.body.clientWidth;
        $.ajax(url, {
            data: param,
            crossDomain: true == !(document.all),
            xhrFields: {
                withCredentials: true
            },
            dataType: 'json',
            type: method,
            timeout: 30000,
            beforeSend: function () {
                if (window.deviceClientWidth < 1200) {
                    Vue.prototype._beforeSendAjax();
                }
            },
            complete: function () {
                if (window.deviceClientWidth < 1200) {
                    Vue.prototype._completeAjax();
                }
            },
            success: function (response) {
                delete window.canRequest[callback];
                if (response && response.hasOwnProperty('return_code')) {
                    callback(response);
                } else {
                    console.log('Incorrect data format');
                }
                if (window.deviceClientWidth < 1200) {
                    Vue.prototype._completeAjax();
                }
            },
            error: function (xhr, type, errorThrownhr) {
                delete window.canRequest[callback];
                // console.log(new Date() + '【AJAX:ERR】-|T:' + type + '|H:' + errorThrownhr);
                if (window.deviceClientWidth < 1200) {
                    Vue.prototype._completeAjax();
                }
            }
        }); //ajax end
    }
}

/***
 * Check the str is null
 * @param str
 * @returns {boolean}
 * @private
 */
function _checkIsNull(str) {
    if (!str || str == "" || str.replace(/(^\s*)|(\s*$)/g, "") == "") {
        return true;
    } else {
        return false;
    }
}

/***
 * Request aliyun to send verification code sms
 * @param id
 * @param mobile
 * @param token
 * @param type
 * @param country_code
 * @returns {boolean}
 * @private
 */
function _getCode(id, mobile, token, type, country_code) {

    if (_checkIsNull(mobile)) {
        toastr.warning(gettext('Incorrect mobile'));
        return false;
    }

    if (typeof(type) == "undefined" || typeof(type) == null || type == "") {
        type = "";
    }

    Vue.nextTick(function () {
        app.isGetCodeForbid = true;
    })

    var pare = {
        mobile: mobile,
        type: type,
        csrfmiddlewaretoken: token
    };

    if (country_code) {
        pare.country_code = country_code;
    }

    _dqRequest('/api/auth/vcode/', 'POST', pare, function (r) {
        if (r.hasOwnProperty('return_code')) {
            if (r.return_code == 0) {
                toastr.success(gettext(r.return_message));
                _leftTimeShort(id);
            } else {
                toastr.error(r.return_message);
                return false;
            }
        }
        else {
            toastr.error(r);
            return false;
        }

    });
}

$(function () {
    $("#avatarDropdown").hover(
        function () {
            $(this).addClass("open");
            $(".user-arrow-blue").css({'display': 'inline-block'});
            $(".user-arrow").css({'display': 'none'});
        }, function () {
            $(this).removeClass("open");
            $(".user-arrow").css({'display': 'inline-block'});
            $(".user-arrow-blue").css({'display': 'none'});
        });
});

/***
 * User Logout
 */
function userLogout() {
    var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
    _dqRequest('/api/auth/logout/', 'POST', {
        csrfmiddlewaretoken: csrfmiddlewaretoken
    }, function (r) {
        if (r.return_code == 0) {

            toastr.success(gettext("Logout success"));

            localStorage.clear();

            setTimeout(function () {
                window.location.href = '/';
            }, 1000);

        } else {
            toastr.error(r.return_message);
        }
    });
}