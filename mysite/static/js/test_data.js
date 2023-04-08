var container = document.getElementById("test_form")
var btnData = document.getElementById("data");
var authorText = document.getElementById("author");
var workTime = document.getElementById("work_time");
var questionsCount = document.getElementById("questions_count");
var difficulty = document.getElementById("difficulty");
var btnDataBlock = document.getElementById("btn_data_block");

btnData.addEventListener('click', function() {
	var request = new XMLHttpRequest();

	request.open('GET', dataUrl);

	request.onload = function() {
		var data = JSON.parse(request.responseText);
		testData = data["data"];

		render(testData);
	}

	request.send();
});

function render(data) {
	authorText.innerHTML = "";
	workTime.innerHTML = "";
	questionsCount.innerHTML = "";
	difficulty.innerHTML = "";
	btnDataBlock.innerHTML = "";

	var htmlForm = "";

	htmlForm += '<form method="POST">';
	htmlForm += csrfToken;

	for (i = 0; i < data.length; i++) {
		htmlForm += '<p><b>' + Object.keys(data[i]) + '</b></p>';

		for (var j in data[i]) {
			console.log(data[i][j])
			for (var k in data[i][j]) {
				htmlForm += '<label>' + data[i][j][k] + '<input type="radio" name="answer" value="' + data[i][j][k] + '"></label>';
			}
		}
	}

	htmlForm += '<div id="btn_save_block"><button type="submit" id="save">Узнать результаты</button></div>';
	htmlForm += '</form>';

	container.insertAdjacentHTML('beforeend', htmlForm);
}