//이미지 파일 처리하는 함수
function loadFile(input) {
    let file = input.files[0]; // 선택된 파일 가져오기

    let newImage = document.createElement("img"); // 새로운 이미지 추가

    newImage.src = URL.createObjectURL(file); //이미지 source 가져오기

    newImage.style.width = "100%";
    newImage.style.height = "100%";
    newImage.style.objectFit = "scale-down";

    let container = document.getElementById('image-show'); //이미지를 image-show div 에 추가

    if (container.children.length == 0) { //첨부된 이미지 파일이 없다면,
        container.appendChild(newImage); //이미지 나오게 하기
    } else {
        container.removeChild(container.children[0]) //이미 이미지가 있다면 이미지를 삭제하고
        container.appendChild(newImage); //새로운 이미지 사진 나오게 하기
    }

}

function posting() {
    let title = $('#title').val()
    let desc = $("#desc").val()
    let file = $('#file')[0].files[0]

    // 이미지,제목,내용 중에 하나라도 빠졌을 경우에 alert 뜨게하기
    if (file == undefined) {
        alert("이미지를 첨부해주세요!")
        return;
    } else if (title == "") {
        alert("제목을 작성해주세요!")
        return;
    } else if (desc == "") {
        alert("내용을 작성해주세요!")
        return;
    }

    let form_data = new FormData();

    form_data.append("file_give", file)
    form_data.append("title_give", title)
    form_data.append("desc_give", desc)

    $.ajax({
        type: "POST",
        url: "/api/posts",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["msg"])
            window.location.href = '/';
        }
    });
}