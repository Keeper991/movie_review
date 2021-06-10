let movie_id;




const otherReviewStarOn = () => {
    const others = document.querySelectorAll(".other_review");
    for (let i = 0; i < others.length; i++) {
        const starVal = others[i].querySelector(".star-val").innerText;
        const starPadding = others[i].querySelector(".star-padding");
        for (let j = 0; j < starVal; j++) {
            starPadding.querySelector(`.starR:nth-child(${j + 1})`).classList.add('on');
        }
    }
}

const myReviewStarOn = () => {
    const review = document.querySelector('.my-review');
    const starVal = review.querySelector('div > span').innerText;
    for (let i = 0; i < starVal; i++) {
        review.querySelector(`.starR:nth-child(${i + 1})`).classList.add('on');
    }
}

// $('.starRev span').click(function () {
//     $(this).parent().children('span').removeClass('on');
//     $(this).addClass('on').prevAll('span').addClass('on');
//     return false;
// });


function saving_review() {
    let star = $('#inputs').val()
    let desc = $('#description').val()
    let id = document.location.href.split("=")[1]

    $.ajax({
        type: "POST",
        url: "/api/review/create",
        data: {star_give: star, desc_give: desc, id_give: id},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
}

const handleReviewDelBtn = () => {
  const movieId = window.location.href.split("=")[1];
  const userId = document.querySelector("#header__user-info a").href.split('=')[1];
  const data = {
    user_id: userId,
    movie_id: movieId,
  };


  $.ajax({
    type: "POST",
    url: "/api/review/delete",
    data: data,
    success: (res) => {
      alert(res["msg"]);
      window.location.reload();
    },
  });
};

function modify_review(event) {
    const my_review = event.target.parentNode.parentNode;
    const desc = my_review.querySelector("div > h6:nth-child(3)");
    const desc_text = desc.innerText;

    const star = my_review;

    star.outerHTML = `<div class="input-group mb-3">
    <select class="form-select" id="modify-inputs">
        <option>별점</option>
        <option value="1">1점 ★</option>
        <option value="2">2점 ★★</option>
        <option value="3">3점 ★★★</option>
        <option value="4">4점 ★★★★</option>
        <option value="5">5점 ★★★★★</option>
    </select>
    <input type="text" class="form-control" id="review_desc_input" value="${desc_text}">
    <div align="right">
        <button type="button" onclick="modify_confirm()" id="button-color" class="btn btn-warning">확인
                    </button>
        <button type="button" onclick="modify_cancel()" id="button-color" class="btn btn-warning">취소
                    </button>
    </div>
</div>`
}

function modify_confirm() {
    let desc = $('#review_desc_input').val()
    let star = $('#modify-inputs').val()

    const movieId = window.location.href.split("=")[1];
    const userId = document.querySelector("#header__user-info a").href.split('=')[1];

    const data = {
        user_id: userId,
        movie_id: movieId,
        review_desc: desc,
        review_star: star
    }

    $.ajax({
        type: "POST",
        url: "/api/review/update",
        data: data,
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
}

function modify_cancel() {
    window.location.reload()
}

// 로그아웃은 내가 가지고 있는 토큰만 쿠키에서 없애면 됩니다.
function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}

function go_main() {
    window.location.href = '/'
}

(function() {
    otherReviewStarOn()
    myReviewStarOn()
})();