function hideAndShowLoginAndUser() {
    let user = document.querySelector('#user');
    if (user.innerHTML != 'anonimowy') {
        document.querySelector('#login').style.display = 'none';
        document.querySelector('#logout').style.display = 'block';
        document.querySelector('#newuser').style.display = 'none';
    } else {
        document.querySelector('#login').style.display = 'block';
        document.querySelector('#logout').style.display = 'none';
        document.querySelector('#newuser').style.display = 'block';
    }
}

function hide() {
    document.querySelectorAll('.all').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelectorAll('.end').forEach(div => {
        div.style.display = 'block';
    });
}

function showResult() {
    document.querySelector('#success').style.display = 'block'
}

function postInput(section, dict) {
    const data = dict
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };

    fetch(`/${section}`, options)
        .then(response => response.json())
        .then(json => {
            let j = json;
            document.querySelector('#success').innerHTML = j.results[0]
            document.querySelector('#uq').innerHTML = j.results[1]
            let done = j.results[0]
            console.log(done)
            if (done === 'fertig') { hide() }
        })
}

function showSection(section) {
    fetch(`/${section}`)
        .then(response => response.text())
        .then(text => {
            if (section == 'all_questions') {
                document.querySelector('#p').innerHTML = ''
                sample = JSON.parse(text);
                t = ''
                for (let i in sample["Q"]) {
                    t = '<dl>' + sample["Q"][i] + '</dl>';
                    document.querySelector('#p').innerHTML += t;
                }
            } else if (section == 'learn') {
                document.querySelector('#uq').innerHTML = text;
            } else if (section == 'new_vocab') {
                console.log('diffrent story');

            } else if (section == 'rank') {
                document.querySelector('#u').innerHTML = ''
                let u = JSON.parse(text);
                t = ''
                let users = u['users']
                for (let i in users) {
                    t = '<dl>' + users[i] + '</dl>';
                    document.querySelector('#u').innerHTML += t;
                }


            }
        })
}

function showPage(page) {
    document.querySelectorAll('.spa').forEach(d => {
        d.style.display = 'none';
    });
    document.querySelector(`#${page}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.click').forEach(button => {
        button.onclick = function() {
            if (this.dataset.page === 'submit_answer') {
                text = document.getElementById('usa').value
                var dict = { 'userAnswer': text };
                showResult();
                postInput(this.dataset.page, dict)
                document.querySelector('#uq').innerHTML = 'text';
                document.getElementById('usa').value = '';
            } else if (this.dataset.page === 'qa') {
                var question = document.getElementById('q').value;
                var answer = document.getElementById('a').value;
                var dictQA = { 'question': question, 'answer': answer }
                postInput(this.dataset.page, dictQA);
                document.getElementById('q').value = '';
                document.getElementById('a').value = '';
            } else if (this.dataset.page === 'page6') {
                console.log('six')
                hide()
<<<<<<< HEAD
<<<<<<< HEAD
            } else if (this.dataset.page === 'user') {
                showPage(this.dataset.page);
=======
>>>>>>> parent of ffb7632... new code from macbook
=======
>>>>>>> parent of ffb7632... new code from macbook
            } else {
                showSection(this.dataset.page);
                showPage(this.dataset.page);
            }
        }
    })
<<<<<<< HEAD
<<<<<<< HEAD
    hideAndShowLoginAndUser()
=======
    let submitLog = document.querySelector('.log');
    submitLog.onclick = hideAndShowLoginAndUser()
>>>>>>> parent of ffb7632... new code from macbook
=======
    let submitLog = document.querySelector('.log');
    submitLog.onclick = hideAndShowLoginAndUser()
>>>>>>> parent of ffb7632... new code from macbook
});