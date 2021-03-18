window.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

document.getElementById('go_home').addEventListener('click', function () {
    location.href = '/';
});

document.getElementById('hide_other').addEventListener('click', function () {
    document.getElementById('main_h1').style.display = 'none';
    document.getElementById('result_title').style.display = 'none';
    document.getElementById('go_home').style.display = 'none';
    document.getElementById('hide_other').style.display = 'none';
});
