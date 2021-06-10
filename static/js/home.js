$(document).ready(function () {
    showArticles();
});

function showArticles() {
    $.ajax({
        type: "GET",
        url: "/movies",
        data: {},
        success: function (response) {
            let movie_list = response['movie_list']
            movie_list.sort(function (a, b) {
                return b['star_avg'] - a['star_avg']
            })
            for (let i = 0; i < movie_list.length; i++) {
                let title = movie_list[i]['movie_title']
                let image = movie_list[i]['movie_img']
                let id = movie_list[i]['movie_id']
                let avg = movie_list[i]['star_avg']
                let rank = movie_list[i]['kino_rank']

                let temp_html = `<div class="card"  style=" cursor: pointer;" onclick="location.href='/detail?id=${id}';">
                                    <img class="card-img-top"
                                         src="${image}"
                                         alt="Card image cap">
                                    <div class="card-body">
                                        <a class="card-title">${title}</a> <br>
                                        <a class="card-title">순위: ${rank}</a>
                                        <p class="card-text comment">영화 평점: ${avg}</p>
                                    </div>
                                </div>
                    `
                $('#cards-box').append(temp_html)
            }
        }
    })
}