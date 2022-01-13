function go_register() {
    //replace(/ /gi,'') 공백제거
    let nickname = $('#nickname').val().replace(/ /gi, '')
    let user_id = $('#id').val().replace(/ /gi, '')
    let password = $('#password').val().replace(/ /gi, '')
    let re_password = $('#re_password').val().replace(/ /gi, '')

    if (nickname === '') {
        alert('닉네임을 입력해주세요:)');
    } else if (user_id === '') {
        alert('아이디를 입력해주세요:)');
    } else if (password === '') {
        alert('비밀번호를 입력해주세요:)');
    } else if (!checkpw(password)) {
        alert('비밀번호는 숫자와 영문을 포함하여8자 이상이어야합니다.');
    } else if (re_password === '') {
        alert('비밀번호를 다시 한번 입력해주세요:)');
    } else if (password !== re_password) {
        alert('비밀번호가 동일하지 않습니다.')
    } else {
        $.ajax({
            type: "POST",
            url: "/api/signup",
            data: {give_nickname: nickname, give_id: user_id, give_pw: password},
            success: function (response) {
                alert(response["msg"]);
                window.location.href = '/';
            }
        })
    }

}

function check_nickname() {
    let nickname = $('#nickname').val()
    if (!nickname) {
        alert('닉네입을 입력해주세요')
    } else {
        $.ajax({
            type: "POST",
            url: `/api/check_nickname`,
            data: {'give_nickname': nickname},
            success: function (response) {
                if (response['overlap'] === 'pass') {
                    alert('사용 가능한 닉네임입니다.')
                } else {
                    alert('사용 중인 닉네임입니다.');
                    $('#nickname').val('')
                    $('#nickname').focus()
                }
            }
        })
    }
}

function check_id() {
    let user_id = $('#id').val()
    if (!user_id) {
        alert('아이디 입력해주세요')
    } else {
        $.ajax({
            type: "post",
            url: `/api/check_id`,
            data: {'give_id': user_id},
            success: function (response) {
                if (response['overlap'] === 'pass') {
                    alert('사용 가능한 아이디입니다.')
                } else {
                    alert('사용 중인 아이디입니다.');
                    $('#id').val('')
                    $('#id').focus()
                }
            }
        })
    }
}


// 비밀번호 영문 숫자 포함 8글자 이상 조건
function checkpw(password) {
    let regpw = /^(?=.*?[a-z])(?=.*?[0-9]).{8,}$/;
    return regpw.test(password)
}

