document.addEventListener('DOMContentLoaded', function() {
    let button = document.getElementById('button-addon2')
    let clearButton = document.getElementById('clear')
    
    button.addEventListener('click', function(){
        let expression = document.getElementById('floatingInputGroup1').value
        fetch('/differentiate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: expression })
        })
        .then(function(response) {
            return response.json()
        })
        .then(function(data) {
            document.getElementById('output-result').innerText = data.result
            document.getElementById('output-box').style.display = 'block'
        })
    })

    clearButton.addEventListener('click', function(){
        document.getElementById('output-box').style.display = 'none'
        document.getElementById('output-result').innerText = ''
    })
});