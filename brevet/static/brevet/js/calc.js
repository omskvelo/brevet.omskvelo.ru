let inputs = document.querySelectorAll('input')

const distanceDom = document.querySelector('#distance')
const distanceFinishDom = document.querySelector('#distance-finish')

const startDom = document.querySelector('#start')
const finishDom = document.querySelector('#finish')

const container = document.querySelector('form')
const insertionPoint = document.querySelector('#insertionPoint')


let controls = [

]

const limits = {
    '200':  13.5,
    '300':  20,
    '400':  27,
    '600':  40,
    '1000': 75
}

//Populate DOM from URL
let url = new URL(window.location.href)
let i = 0;

if (url.searchParams.get("start")) startDom.value = url.searchParams.get("start")
if (url.searchParams.get("distance")) distanceDom.value = url.searchParams.get("distance")
if (url.searchParams.get("cp")){
    url.searchParams.get("cp").split(",").map(Number).forEach(control =>{
        if (control){
            if (i + 1 >= controls.length) add_cp_dom()
            controls[i].distanceDom.value = control
            i++
        }
    })
}

function refresh(){
    // Calculate
    start = startDom.value
    distance = distanceDom.value

    distanceFinishDom.value = distance
    finishDom.value = `c ${calculate_control_open(start,distance)} по ${calculate_finish_close(start,distance)}`

    controls.forEach(control => {
        let km = control.distanceDom.value
        if (km){
            control.timeDom.value = `c ${calculate_control_open(start,km)} по ${calculate_control_close(start,km)}`
        }
        else{
            control.timeDom.value = ""
        }
    })

    //Update URL
    let cp = "";
    controls.forEach(control => {
        cp += control.distanceDom.value
        cp += ","
    })
    cp = cp.slice(0,-2)

    manage_url_param("distance", distanceDom.value)
    manage_url_param("start", startDom.value)
    manage_url_param("cp", cp)
    
    window.history.pushState({}, '', url)

    // Update DOM
    if (controls[controls.length-1].distanceDom.value != ""){
        add_cp_dom()
    }
    while (controls[controls.length-1].distanceDom.value == ""
        && controls[controls.length-2].distanceDom.value == ""){
            remove_cp_dom(controls.length-1)
        }
}

function manage_url_param(name, value){
    if (value) {
        if (url.searchParams.get(name)!= null) url.searchParams.set(name, value)
        else url.searchParams.append(name, value)        
    }
    else url.searchParams.delete(name)
}

function calculate_control_open(time, km){
    let hr = Number(time.split(":")[0])
    let min =  Number(time.split(":")[1])
    let t = hr + min/60

    t += Math.min(km,200)/34
    t += Math.min(Math.max(km-200,0),200)/32
    t += Math.min(Math.max(km-400,0),200)/30
    t += Math.min(Math.max(km-600,0),400)/28
    t += Math.min(Math.max(km-1000,0),200)/26
    t += Math.min(Math.max(km-1200,0),600)/25
    t += Math.min(Math.max(km-1800,0),200)/24

    return format_time(t)
}

function calculate_control_close(time, km){
    let hr =  Number(time.split(":")[0])
    let min =  Number(time.split(":")[1])
    let t = hr + min/60

    t += 1
    t += Math.min(km,60)/20
    t += Math.min(Math.max(km-60,0),540)/15
    t += Math.min(Math.max(km-600,0),400)/11.428
    t += Math.min(Math.max(km-1000,0),200)/13.333
    t += Math.min(Math.max(km-1200,0),200)/11
    t += Math.min(Math.max(km-1400,0),400)/10
    t += Math.min(Math.max(km-1800,0),200)/9

    return format_time(t)
}

function calculate_finish_close(time, km){
    if (limits[String(km)]) {
        let hr = Number(time.split(":")[0])
        let min =  Number(time.split(":")[1])
        let t = hr + min/60
        t += limits[String(km)]
        return format_time(t)
    }
    else return calculate_control_close(time, km)
}

function format_time(t){
    let hr = Math.floor(t % 24)
    let min = Math.round(t % 1 * 60)
    let days = Math.floor(t / 24)
    
    if (min == 60){
      hr += 1
      min = 0
    }
    
    hr = String(hr).padStart(2,"0")
    min = String(min).padStart(2,"0")
    
    if (days === 0) days = ""
    else days = ` (+${days})`

    return `${hr}:${min}${days}`
}

function add_cp_dom(){
    const index = controls.length + 1
    let floatTop = document.createElement("div")
    floatTop.setAttribute('class', 'form-floating')

    let inputTop = document.createElement("input")
    inputTop.setAttribute('type', 'number')
    inputTop.setAttribute('class', 'form-control joined_field_upper')
    inputTop.setAttribute('id',`distance${index}`)
    inputTop.setAttribute('placeholder', "_")
    inputTop.addEventListener('input', refresh)
    inputTop.onkeyup = function(e) {
        if(e.key == "Enter"){
            controls[index].distanceDom.focus()
        }
    }
    inputTop.onfocus = function(e) {
        temp = inputTop.value
        inputTop.value = ""
        inputTop.value = temp
    }

    let labelTop = document.createElement("label")
    labelTop.setAttribute('for', `distance${index}`) 
    labelTop.textContent = `КП${index}, км`

    let floatBottom = document.createElement("div")
    floatBottom.setAttribute('class', 'form-floating')

    let inputBottom = document.createElement("input")
    inputBottom.setAttribute('type', 'text')
    inputBottom.setAttribute('class', 'form-control joined_field_lower')
    inputBottom.setAttribute('id',`control${index}`)
    inputBottom.setAttribute('placeholder', "_")
    inputBottom.setAttribute('disabled','')
    inputBottom.addEventListener('input', refresh)

    let labelBottom = document.createElement("label")
    labelBottom.setAttribute('for', `control${index}`)
    labelBottom.textContent = "Время"

    floatTop.append(inputTop,labelTop)
    floatBottom.append(inputBottom,labelBottom)
    container.insertBefore(floatTop, insertionPoint)
    container.insertBefore(floatBottom, insertionPoint)

    controls[index-1] = {
        timeDom: document.querySelector(`#control${index}`),
        distanceDom: document.querySelector(`#distance${index}`)
    }

    inputs = document.querySelectorAll('input')
}

function remove_cp_dom(index){
    controls[index].timeDom.parentElement.remove()
    controls[index].distanceDom.parentElement.remove()
    controls.splice(index,1)
}

inputs.forEach(input => input.addEventListener('input', refresh))

add_cp_dom()
refresh()

function test_calc(){
    // Check results against reference dataset: https://www.audax-club-parisien.com/en/our-organizations/brm-world/
    // Specifically http://www.audax-club-parisien.com/download/plages_horaires_brm_10_FR.xls
    console.assert(calculate_control_open("07:00", 35) === "08:02", "Test failed!")
    console.assert(calculate_control_open("07:00", 155) === "11:34", "Test failed!")
    console.assert(calculate_control_open("18:00", 155) === "22:34", "Test failed!")
    console.assert(calculate_control_open("18:00", 205) === "00:02 (+1)", "Test failed!")
    console.assert(calculate_control_open("00:00", 442) === "13:32", "Test failed!")
    console.assert(calculate_control_open("00:00", 699) === "22:20", "Test failed!")
    console.assert(calculate_control_open("10:00", 1001) === "19:07 (+1)", "Test failed!")
    console.assert(calculate_control_open("10:00", 1190) === "02:24 (+2)", "Test failed!")

    console.assert(calculate_control_close("07:00", 35) === "09:45", "Test failed!")
    console.assert(calculate_control_close("07:00", 155) === "17:20", "Test failed!")
    console.assert(calculate_control_close("18:00", 155) === "04:20 (+1)", "Test failed!")
    console.assert(calculate_control_close("18:00", 205) === "07:40 (+1)", "Test failed!")
    console.assert(calculate_control_close("00:00", 442) === "05:28 (+1)", "Test failed!")
    console.assert(calculate_control_close("00:00", 699) === "00:40 (+2)", "Test failed!")
    console.assert(calculate_control_close("10:00", 1190) === "03:15 (+4)", "Test failed!")

    console.assert(calculate_finish_close("07:00", 200) === "20:30", "Test failed!")
    console.assert(calculate_finish_close("07:00", 300) === "03:00 (+1)", "Test failed!")
    console.assert(calculate_finish_close("18:00", 400) === "21:00 (+1)", "Test failed!")
    console.assert(calculate_finish_close("18:00", 600) === "10:00 (+2)", "Test failed!")
    console.assert(calculate_finish_close("00:00", 700) === "00:45 (+2)", "Test failed!")
    console.assert(calculate_finish_close("00:00", 900) === "18:15 (+2)", "Test failed!")
    console.assert(calculate_finish_close("10:00", 1000) === "13:00 (+3)", "Test failed!")
}