// create.html
let list = document.getElementById('list');

let newListLabel = document.getElementById('newListLabel');

list.onchange = function(event)  {

    if (event.currentTarget.value == 'other') {

        newListLabel.classList.remove('hidden');
        console.log('hi');
    } else {
        newListLabel.classList.add('hidden');
    }
}



// viewtodos.html
let checkbox = document.getElementsByClassName('checkbox');

let checked = false;

let checks = document.getElementsByClassName('checkbox');

console.log(checks);

for (let i=0;i<checks.length;i++) {

    checks[i].addEventListener('click',function(){
        if (checked == false) {
            checks[i].src = 'check.png';
            checked = true;

        } else {
            checks[i].src = 'blank-check-box.png';
            checked=false;
        }

        
    })
}