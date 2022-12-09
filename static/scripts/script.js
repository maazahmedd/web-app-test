// create.html
let list = document.getElementById('list');

if (list !== null) {
    let newListLabel = document.getElementById('newListLabel');

    list.onchange = function(event)  {

        if (event.currentTarget.value == 'other') {

            newListLabel.classList.remove('hidden');
            console.log('hi');
        } else {
            newListLabel.classList.add('hidden');
        }
    }
}

// viewtodos.html



let checks = document.getElementsByClassName('checkbox');

if (checks.length !== 0) {

checked = []

    for (let i = 0; i < checks.length; i++) {
        checked.push(false);
    }

    for (let i = 0; i < checks.length; i++) {

        checks[i].addEventListener('click', function(){
            console.log('clicked');
            if (checked[i] == false) {
                checks[i].src = 'static/images/check.png';
                checked[i] = true;

            } else {
                checks[i].src = 'static/images/blank-check-box.png';
                checked[i] = false;
            }
        })
    }

}


let button = document.getElementsByTagName('button');

for (let i=0;i<button.length;i++){
    button[i].addEventListener('click',function(){
        console.log('clicked');
    })
}




let signupB = document.getElementById('signupB');


let signupForm = document.getElementById('signupForm');

if (signupB && signupForm != null) {

    signupB.addEventListener('click',function(){

        signupForm.submit();
        console.log(signupForm.value);
    
    })

}

