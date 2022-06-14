const time_input = document.querySelector("#floatingInput")
const form = document.querySelector(".form-send-result")
const error = document.querySelector("#js_error")

function continuous_validation(event) {
    switch(time_input.value.length){
        case 1:
            if (!time_input.value.match(/^\d$/)){
                time_input.value = ""
            }
            else if (time_input.value.match(/^[^012]$/)){
                time_input.value = "0"+time_input.value
            }
            break
        case 2:
            if (!time_input.value.match(/^\d\d$/)){
                time_input.value = "0"+time_input.value
            }    
            break
        case 3:
            if (time_input.value.match(/^\d\d\d/)){
                time_input.value = time_input.value.slice(0,2) + ":" + time_input.value.slice(2,3)
            }
            else if (time_input.value.match(/^\d\d[^\d]$/)){
                time_input.value = time_input.value.slice(0,2) + ":"
            }  
            break
        case 4:
            if (!time_input.value.match(/^\d\d:\d$/)){
                time_input.value = time_input.value.slice(0,3)
            }  
            break 
        case 5:
            if (!time_input.value.match(/^\d\d:\d\d$/)){
                time_input.value = time_input.value.slice(0,4)
            }  
            break 
    }
}

function submit_validation(event){
    if (!time_input.value.match(/^\d{1,2}:\d\d$/)){
        event.preventDefault()
        error.innerText = "Введите корректное время."
    }  
}

time_input.addEventListener('input', continuous_validation)
form.addEventListener('submit', submit_validation)