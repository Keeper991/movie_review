const handleLogout = () => {
    $.removeCookie('mytoken', { path: '/' });
    alert('로그아웃 되었습니다');
    window.location.href = '/login';
}

$("#header__logout-btn").on('click', handleLogout)