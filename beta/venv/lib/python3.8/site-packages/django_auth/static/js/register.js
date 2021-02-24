var app = new Vue({
    el: '#app',
    data: {
        uRegister: {
            country_code:'+86',
            phone: '',
            msgcode: '',
            username: '',
            password: '',
            agree: true
        },
    },
    methods: {
        check_country_code:function() {
            var country_code = $("#country_code").val();
            var new_country_code1 = country_code.substring(1,country_code.length).replace(/[^0-9]/g,'');
            $("#country_code").val("+" + new_country_code1);
            var new_country_code2 = $("#country_code").val();
            if(new_country_code2.length>8) {
                $("#country_code").val("+" + new_country_code2.substring(0, 8));
            }
        },
        setBorderGrey: function() {
            var inputs = $(".form-lr-input-style");
            for(var i=0; i< inputs.length; i++) {
                if($(inputs[i]).val()!="") {
                    $(inputs[i]).addClass('input-border-grey');
                } else {
                    $(inputs[i]).removeClass('input-border-grey');
                }
            }
        },
        getMobileCode:function(id){

            var country_code = $("#country_code").val();
            var reg = new RegExp("^[0-9]*$");
            if(country_code.length<2) {
                toastr.warning(gettext('Incorrect mobile'));
                return false;
            }

            var mobile = $("input[name='mobile']").val();
            if(mobile.replace(/[^0-9]/g,'').length >= 4){
                app.isGetCodeForbid = false;
            } else {
                app.isGetCodeForbid = true;
            }

            if(app.isGetCodeForbid){
                toastr.warning(gettext('请填写正确的手机号！'));
                return false;
            }


             var mobile = $("input[name='mobile']").val();
             var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
             _getCode(id,mobile,csrfmiddlewaretoken,"register", country_code);
        },
        checkPhone:function(id){
            var mobile = $("input[name='mobile']").val();
            if(mobile.replace(/[^0-9]/g,'').length >= 4){
                app.isGetCodeForbid = false;
            } else {
                app.isGetCodeForbid = true;
            }

            app.checkInput();
        },
        checkInput: function() {
            app.setBorderGrey();
            Vue.nextTick(function() {
                if(app.uRegister.phone!="" && app.uRegister.msgcode!="" && app.uRegister.username!="" && app.uRegister.password!="" && app.uRegister.agree) {
                    app.isSubmitForbid = false;
                } else {
                    app.isSubmitForbid = true;
                }
            });
        },
        userRegister:function() {

            var mobile = $("input[name='mobile']").val();
            var mobilecode = $("input[name='mobilecode']").val();
            var username = $("input[name='username']").val();
            var password = $("input[name='password']").val();
            var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
            var country_code = $("#country_code").val();

            username = username.replace(/^\s+|\s+$/g,"");
            password = password.replace(/\s+/g,"");

            var reg = new RegExp("^[0-9]*$");
            if(country_code.length<2) {
                toastr.warning(gettext('Incorrect country code'));
                return false;
            }


            if(_checkIsNull(mobile)){
                toastr.warning(gettext('Incorrect mobile'));
                return false;
            }

            var mobile = $("input[name='mobile']").val();

            if(mobile.replace(/[^0-9]/g,'').length < 4){
                toastr.warning(gettext('Incorrect mobile'));
                return false;
            }

            if(_checkIsNull(mobilecode)){
                toastr.warning(gettext('Verity code is empty'));
                return;
             }

            if(mobilecode.length != 4){
                 toastr.warning(gettext('Verity code must be 1 to 20 characters'));
                 return;
            }

             if(username.length <1 || username.length>20){
                 toastr.warning(gettext('Username must be 1 to 20 characters'));
                 return;
             }

             if(password.length <6 || password.length>20){
                 toastr.warning(gettext('Password must be 6 to 20 characters'));
                 return;
             }

             _dqRequest('/api/auth/register/', 'POST', {
                 mobile: mobile,
                 country_code: country_code,
                 username: username,
                 password: password,
                 mobilecode: mobilecode,
                 csrfmiddlewaretoken: csrfmiddlewaretoken
             }, function(r) {
                 if(r.return_code==0) {

                     toastr.success(gettext("Register Success"));
                     setTimeout(function(){
                        window.location.href = '/';
                     }, 2000);

                 } else {
                     toastr.error(r.return_message);
                 }
             });
        }
    }
});


