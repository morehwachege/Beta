var app = new Vue({
    el: '#app',
    data: {
        uLogin: {
            mobile: '',
            mobilecode: '',
            username: '',
            password: ''
        },
    },
    methods: {
        userLogin: function () {

            var pare = {
                username: "",
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            };
            var username = $("input[name='username']").val();
            var password = $("input[name='password']").val();
            username = username.replace(/^\s+|\s+$/g, "");
            password = password.replace(/\s+/g, "");
            if (username.length < 1 || username.length > 20) {
                toastr.warning(gettext('Username must be 1 to 20 characters'));
                return;
            }
            if (password.length < 6 || password.length > 20) {
                toastr.warning(gettext('Password must be 6 to 20 characters'));
                return;
            }

            pare.username = username.replace(/(^\s*)|(\s*$)/g, "");
            pare.password = password.replace(/(^\s*)|(\s*$)/g, "");

            _dqRequest('/api/auth/login/', 'POST', pare, function (r) {
                if (r.return_code == 0) {

                    if (app.keepLogin) {
                        localStorage.setItem('keep_login', true);
                    } else {
                        localStorage.clear();
                    }

                    toastr.success(gettext("Login success"));

                    setTimeout(function () {
                        window.location.href = '/';
                    }, 1000);

                } else {
                    toastr.error(r.return_message);
                }
            });

        }
    }
});