window.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

document.getElementById('go_home').addEventListener('click', function () {
    location.href = '/';
});

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

document.getElementById('hide_other').addEventListener('click', function () {
    document.getElementById('main_h1').style.display = 'none';
    document.getElementById('result_title').style.display = 'none';
    document.getElementById('go_home').style.display = 'none';
    document.getElementById('download_it').style.display = 'none';
    document.getElementById('hide_other').style.display = 'none';
});

document.getElementById('download_it').addEventListener('click', function () {
    download('data.txt', document.getElementById('result').innerText);
});