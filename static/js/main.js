
// index page js
$(document).ready(function () {
    listing();
});

function listing() {
    $.ajax({
        type: "GET",
        url: "/buckets",
        data: {},
        success: function (response) {
            let buckets = response['all_buckets']
            for (let i = 0; i < buckets.length; i++) {
                let title = buckets[i]['title']
                let desc = buckets[i]['desc']
                let file = buckets[i]['file']
                let id = buckets[i]['_id']

                let temp_html = `<div class="card" onclick="listing_detail('${id}')" style="cursor: pointer">
                                                <div class="img-wrap">
                                                    <img src="../static/${file}" class="card-img-top">
                                                </div>
                                                <div class="card-body">
                                                    <h5 class="card-title">${title}</h5>
                                                    <p class="card-text">${desc}</p>
                                                </div>
                                            </div>`
                $('#buckets-box').append(temp_html)
            }
        }
    })
}

function listing_detail(id) {
    $('#bucket-modal-contents').empty()
    $("#bucket-modal").show();
    $.ajax({
        type: "GET",
        url: `/api/bucketdetail?id_give=${id}`,
        data: {},
        success: function (response) {
            let bucket_detail = response['bucket_detail']
            let title = bucket_detail['title']
            let desc = bucket_detail['desc']
            let file = bucket_detail['file']
            let temp_html = `<div class="card">
                                                <div class="close" onclick=$("#bucket-modal").hide()>
                                                    <i class="fa fa-times" aria-hidden="true"></i>
                                                </div>
                                                <img src="../static/${file}" class="card-img-top">
                                                <div class="card-body">
                                                    <h5 class="card-title">${title}</h5>
                                                    <p class="card-text">${desc}</p>
                                                </div>
                                            </div>`
            $('#bucket-modal-contents').append(temp_html)
        }
    })
}

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃 되었습니다!')
    window.location.href = '/'
}

function mp_posting() {
    if ($.cookie('mytoken')) {
        window.location.href = '/posting'
    } else {
        alert('로그인 먼저 부탁드려요~')
        window.location.href = '/login'
    }
}