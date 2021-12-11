
function hide(page) {
    document.querySelectorAll('.spa').forEach(d => {
        d.style.display = 'none';
        //d.style.background-color = 'coral';
    });
}

function postInput(section, dict) {
    const data = dict
    console.log('data json: ', JSON.stringify(data))
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };

    fetch(`/${section}`, options)
        .then(response => response.json())
        .then(json => {
            console.log('json: ', json)
            console.log('options: ', options)
            let j = json;
            document.querySelector('#success').innerHTML = j.results[0]
            document.querySelector('#uq').innerHTML = j.results[1]
            let done = j.results[2]
            if (done == true) { alert('na dziś to wszystko') }
        })
}

function showSection(section) {
    fetch(`/${section}`)
        .then(response => response.text())
        .then(text => {
            if (section == 'page3') {
                document.querySelector('#p').innerHTML = ''
                sample = JSON.parse(text);
                console.log('sample: ', sample["Q"][0])
                t = ''
                for (let i in sample["Q"]) {
                    t = '<dl>' + sample["Q"][i] + '</dl>';
                    document.querySelector('#p').innerHTML += t;
                }
            }
            else if (section == 'page2') {
                document.querySelector('#uq').innerHTML = text;
            }
            else if (section == 'page1') { console.log('diffrent story') }
        })
}

function showPage(page) {
    document.querySelectorAll('.spa').forEach(d => {
        d.style.display = 'none';
    });
    document.querySelector(`#${page}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.click').forEach(button => {
        button.onclick = function () {
            if (this.dataset.page === 'page4') {
                console.log('klniete i porównane', this.dataset.page)
                text = document.getElementById('usa').value
                var dict = { 'userAnswer': text };
                postInput(this.dataset.page, dict)
                document.querySelector('#uq').innerHTML = 'text';
                hide(this.dataset.page);
            }
            else if (this.dataset.page === 'page5') {
                var question = document.getElementById('q').value;
                var answer = document.getElementById('a').value;
                console.log('question and answer: ', question, answer);
                var dictQA = { 'question': question, 'answer': answer }
                postInput(this.dataset.page, dictQA);
            }
            else {
                showSection(this.dataset.page);
                showPage(this.dataset.page);
            }
        }
    })
});

