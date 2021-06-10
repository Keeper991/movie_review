const handleReviewDelBtn = ({ target }) => {
  // 수정할 리뷰의 tr
  const tr = target.parentNode.parentNode;
  tr.outerHTML = "";

  const userId = window.location.href.split("=")[1];
  const movieId = tr.querySelector("a").href.split("=")[1];

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
    },
  });
};

const handleReviewConfirmBtn = ({ target }) => {
  // 수정할 리뷰의 tr
  const tr = target.parentNode.parentNode;
  const desc = tr.querySelector(".review__desc-input");
  const descVal = desc.value;
  const star = tr.querySelector(".review__star-select");
  const starVal = star.value;

  desc.outerText = descVal;
  star.outerText = starVal;

  target.outerHTML = `
    <button class="review__edit-btn">수정</button>
  `;
  $(".review__edit-btn").on("click", handleReviewEditBtn);

  const userId = window.location.href.split("=")[1];
  const movieId = tr.querySelector("a").href.split("=")[1];

  const data = {
    user_id: userId,
    movie_id: movieId,
    review_desc: descVal,
    review_star: starVal,
  };

  $.ajax({
    type: "POST",
    url: "/api/review/update",
    data: data,
    success: (res) => {
      alert(res["msg"]);
    },
  });
};

const handleReviewEditBtn = ({ target }) => {
  // 수정할 리뷰의 tr
  const tr = target.parentNode.parentNode;
  const desc = tr.querySelector(".review__desc");
  const descVal = desc.innerText;
  const star = tr.querySelector(".review__star");
  const starVal = star.innerText;

  desc.innerHTML = `
    <input type="text" class="review__desc-input" value=${descVal}>
  `;
  star.innerHTML = `
    <select class="review__star-select">
      <option value=5>5</option>
      <option value=4>4</option>
      <option value=3>3</option>
      <option value=2>2</option>
      <option value=1>1</option>
    </select>
  `;

  const option = star.querySelector(
    `.review__star-select > option:nth-last-child(${starVal})`
  );
  option.selected = true;

  target.outerHTML = `
    <button class="review__confirm-btn">확인</button>
  `;
  $(".review__confirm-btn").on("click", handleReviewConfirmBtn);
};

// const handleUserDelBtn = () => {
//
// }

const handleNickConfirmBtn = () => {
  const newNick = $("#user__nick-input").val();
  $("#user__nickname").html(`
    <span>${newNick}</span>
    <button id="user__nick-edit-btn">수정</button>
  `);

  $("#user__nick-edit-btn").on("click", handleNickEditBtn);

  const id = $("#user__id").text();

  $.ajax({
    type: "POST",
    url: "/api/user/update/nick",
    data: { user_id: id, user_nick: newNick },
    success: (res) => {
      alert(res["msg"]);
      window.location.reload();
    },
  });
};

const handleNickEditBtn = () => {
  const preNick = $("#user__nickname > span").text();
  $("#user__nickname").html(`
    <input type="text" id="user__nick-input" value="${preNick}"></input>
    <button id="user__nick-confirm-btn">확인</button>
  `);

  $("#user__nick-confirm-btn").on("click", handleNickConfirmBtn);
};

const handleAvatarChange = () => {
  const avatar = $("#avatar-input")[0].files[0];
  const formData = new FormData();
  formData.append("user_img", avatar);
  formData.append("user_id", window.location.href.split("=")[1]);
  $.ajax({
    type: "POST",
    url: "/api/user/update/img",
    data: formData,
    cache: false,
    contentType: false,
    processData: false,
    success: (res) => {
      alert(res["msg"]);
      // $("#user__avatar").attr("src", URL.createObjectURL(avatar));
      window.location.reload();
    },
  });
};

const init = () => {
  $("#avatar-input").on("change", handleAvatarChange);
  $("#user__nick-edit-btn").on("click", handleNickEditBtn);
  $(".review__edit-btn").on("click", handleReviewEditBtn);
  $(".review__del-btn").on("click", handleReviewDelBtn);
};

$(document).ready(init);
