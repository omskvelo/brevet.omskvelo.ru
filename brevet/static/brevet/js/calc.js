let inputs = document.querySelectorAll('input')

const distanceDom = document.querySelector('#distance')
const distanceFinishDom = document.querySelector('#distance-finish')
const distanceFinishDeltaDom = document.querySelector('#distance-finish-delta')
const startDom = document.querySelector('#start')
const finishDom = document.querySelector('#finish')
const container = document.querySelector('form')
const insertionPoint = document.querySelector('#insertionPoint')
const methodDom = document.querySelector('#method')
const methodListDom = document.querySelector('#method-list')
const sourceDom = document.querySelector('#calc-source')
const elevationDom = document.querySelector('#elevation')
const extendedLimitDom = document.querySelector('#extended-limit')

const methods = {
    brm: {
        name: 'BRM',
        source: 'Источник формул: \
        <a href="http://www.audax-club-parisien.com/download/plages_horaires_brm_10_FR.xls" target="_blank"> xls-файл </a>, \
        опубликованный на сайте АСР в разделе \
        <a href="https://www.audax-club-parisien.com/en/our-organizations/brm-world/"> "BRM". </a>'
    },
    lrm: {
        name: 'LRM',
        source: 'Источник формул: \
        <a href="https://www.randonneursmondiaux.org/files/Rules_2019.pdf" target="_blank"> правила LRM </a>'
    },
}



let controls = []

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

let currentMethod = url.searchParams.get("method")     || 'brm'
startDom.value = url.searchParams.get("start")         || '07:00'
distanceDom.value = url.searchParams.get("distance")   || '200'
elevationDom.value = url.searchParams.get("elevation") || '0'

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
    let start = startDom.value
    let distance = distanceDom.value
    let elevation = elevationDom.value

    distanceFinishDom.value = distance

    if (currentMethod == 'brm'){
        finishDom.value = `c ${calculate_control_open(start,distance)} по ${calculate_finish_close(start,distance)}`
        
        for (const [i, control] of controls.entries()){
            let km = control.distanceDom.value

            // Delta fields
            let delta = km
            if (i > 0) {
                delta -= controls[i-1].distanceDom.value
            }
            if (delta >= 0) {
                control.distanceDeltaDom.value = delta
            }
            else {
                control.distanceDeltaDom.value = ""
            }

            // Time fields
            if (km){
                control.timeDom.value = `c ${calculate_control_open(start,km)} по ${calculate_control_close(start,km)}`
            }
            else{
                control.timeDom.value = ""
            }
        }
    }

    if (currentMethod == 'lrm'){
        let limit = calculate_extended_limit(distance, elevation)
        let extra_hours = calculate_lrm_extended_hours(distance, limit)
        extendedLimitDom.value = `${limit}% (${extra_hours})`

        finishDom.value = `c ${calculate_lrm_control_open(start,distance)} по ${calculate_lrm_finish_close(start,distance,distance,limit)}`

        for (const [i, control] of controls.entries()){
            let km = control.distanceDom.value

            // Delta fields
            let delta = km
            if (i > 0) {
                delta -= controls[i-1].distanceDom.value
            }
            if (delta >= 0) {
                control.distanceDeltaDom.value = delta
            }
            else {
                control.distanceDeltaDom.value = ""
            }

            // Time fields
            if (km){
                control.timeDom.value = `c ${calculate_lrm_control_open(start,km)} по ${calculate_lrm_control_close(start,km,distance,limit)}`
            }
            else{
                control.timeDom.value = ""
            }
        }
    }

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
    manage_url_param('method', currentMethod)
    manage_url_param('elevation', elevation)
    
    window.history.pushState({}, '', url)

    // Update DOM
    if (controls[controls.length-1].distanceDom.value != "" || controls[controls.length-1].distanceDeltaDom.value != ""){
        add_cp_dom()
    }
    if (controls[controls.length-2] != undefined){
        while (controls[controls.length-1].distanceDom.value == ""
            && controls[controls.length-2].distanceDom.value == ""){
                remove_cp_dom(controls.length-1)
                if (controls.length == 1) break
            }
    }

    //Calculate finish delta (must be done AFTER DOM update)
    finish_delta = Number(distance)
    if (controls.length > 1){
        finish_delta -= controls[controls.length-2].distanceDom.valueAsNumber
    }
    distanceFinishDeltaDom.value = finish_delta  
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

function calculate_lrm_control_open(time, km){
    let hr = Number(time.split(":")[0])
    let min =  Number(time.split(":")[1])
    let t = hr + min/60

    t += km/30

    return format_time(t)
}

function calculate_lrm_control_close(time, km, distance, limit){
    let hr =  Number(time.split(":")[0])
    let min =  Number(time.split(":")[1])
    let t = hr + min/60
    let dt

    if (distance <= 1299) dt = km/13.3333 
    if (distance >= 1300 && distance <= 1899) dt = km/12
    if (distance >= 1900 && distance <= 2499) dt = km/10
    if (distance >= 2500) dt = km/8.3333
    dt *= (limit + 100)/100

    t += dt
    return format_time(t)
}

function calculate_lrm_finish_close(time, km, distance, limit){
    return calculate_lrm_control_close(time, km, distance, limit)
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

function calculate_extended_limit (distance, elevation){
    if (elevation == "") return 0
    if (distance == 0) return 0
    rate = elevation / distance
    if (rate <= 11) return 0
    return Math.floor((rate - 11))*5
}

function calculate_lrm_extended_hours(distance, limit){
    let hr
    let min
    let km = distance

    if (distance <= 1299) hr = km/13.3333 
    if (distance >= 1300 && distance <= 1899) hr = km/12
    if (distance >= 1900 && distance <= 2499) hr = km/10
    if (distance >= 2500) hr = km/8.3333
    hr *= limit/100

    min = Math.round(hr % 1 * 60)
    hr = Math.floor(hr)

    if (min == 60){
      hr += 1
      min = 0
    }
    
    hr = String(hr).padStart(2,"0")
    min = String(min).padStart(2,"0")

    return `${hr}:${min}`
}

function add_cp_dom(){
    const index = controls.length + 1
    let floatTopLeft = document.createElement("div")
    floatTopLeft.setAttribute('class', 'form-floating')

    let inputTopLeft = document.createElement("input")
    inputTopLeft.setAttribute('type', 'number')
    inputTopLeft.setAttribute('class', 'form-control joined_field_upper_left')
    inputTopLeft.setAttribute('id',`distance${index}`)
    inputTopLeft.setAttribute('placeholder', "_")
    inputTopLeft.addEventListener('input', refresh)
    inputTopLeft.onkeyup = function(e) {
        if(e.key == "Enter"){
            controls[index].distanceDom.focus()
        }
    }
    inputTopLeft.onfocus = function(e) {
        temp = inputTopLeft.value
        inputTopLeft.value = ""
        inputTopLeft.value = temp
    }

    let labelTopLeft = document.createElement("label")
    labelTopLeft.setAttribute('for', `distance${index}`) 
    labelTopLeft.textContent = `КП${index}, км`

    let floatTopRight = document.createElement("div")
    floatTopRight.setAttribute('class', 'form-floating')

    let inputTopRight = document.createElement("input")
    inputTopRight.setAttribute('type', 'number')
    inputTopRight.setAttribute('class', 'form-control joined_field_upper_right')
    inputTopRight.setAttribute('id',`distance${index}-delta`)
    inputTopRight.setAttribute('placeholder', "_")
    inputTopRight.oninput = function(e) {
        km = inputTopRight.valueAsNumber
        if (index > 1){
            km += controls[index-2].distanceDom.valueAsNumber
        }
        inputTopLeft.value = km
    }
    inputTopLeft.onkeyup = function(e) {
        if(e.key == "Enter"){
            controls[index].distanceDom.focus()
        }
    }
    inputTopLeft.onfocus = function(e) {
        temp = inputTopLeft.value
        inputTopLeft.value = ""
        inputTopLeft.value = temp
    }
    inputTopRight.onkeyup = function(e) {
        if(e.key == "Enter"){
            controls[index].distanceDeltaDom.focus()
        }
        refresh()
    }
    inputTopRight.onfocus = function(e) {
        temp = inputTopLeft.value
        inputTopLeft.value = ""
        inputTopLeft.value = temp
    }

    let labelTopRight = document.createElement("label")
    labelTopRight.setAttribute('for', `distance${index}-delta`) 
    labelTopRight.textContent = `До КП${index}, км`

    let formTop = document.createElement("div")
    formTop.setAttribute('class', 'form-twin')

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

    floatTopLeft.append(inputTopLeft,labelTopLeft)
    floatTopRight.append(inputTopRight, labelTopRight)
    formTop.append(floatTopLeft, floatTopRight)
    floatBottom.append(inputBottom,labelBottom)
    container.insertBefore(formTop, insertionPoint)
    container.insertBefore(floatBottom, insertionPoint)

    controls[index-1] = {
        timeDom: document.querySelector(`#control${index}`),
        distanceDom: document.querySelector(`#distance${index}`),
        distanceDeltaDom: document.querySelector(`#distance${index}-delta`)
    }
}

function remove_cp_dom(index){
    controls[index].timeDom.parentElement.remove()
    controls[index].distanceDom.parentElement.remove()
    controls[index].distanceDeltaDom.parentElement.remove()
    controls.splice(index,1)
}

function load_methods(){
    for(let method of Object.getOwnPropertyNames(methods)){
        let li = document.createElement('li')
        let item = document.createElement('button')
        item.setAttribute('class','w-100 dropdown-item')
        item.setAttribute('id', `select-${method}`)
        item.innerText = methods[method]['name']
        item.onclick = e => select_method(method)

        li.append(item)
        methodListDom.append(li)
    }
}

function select_method(method){
    currentMethod = method
    methodDom.innerText = methods[method]['name']
    sourceDom.innerHTML = methods[method]['source']
    if (currentMethod == 'lrm'){
        elevationDom.removeAttribute('hidden')
        extendedLimitDom.removeAttribute('hidden')
    } else {
        elevationDom.setAttribute('hidden',"")
        extendedLimitDom.setAttribute('hidden',"")
    }
    refresh()
}

inputs.forEach(input => input.addEventListener('input', refresh))


add_cp_dom()
load_methods()
select_method(currentMethod)
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

    //Check results against dataset(Appendix 3): https://www.randonneursmondiaux.org/files/Rules_2019.pdf 
    console.assert(calculate_lrm_control_close("07:00", 1440, 1440, calculate_extended_limit(1440, 12200)) === "07:00 (+5)", "Test failed!") //LEL
    console.assert(calculate_lrm_control_close("07:00", 1518, 1518, calculate_extended_limit(1518, 21000)) === "02:09 (+6)", "Test failed!") //Alpi 4000
    console.assert(calculate_lrm_control_close("07:00", 1600, 1600, calculate_extended_limit(1600, 20000)) === "03:00 (+6)", "Test failed!") //1001 Miglia
    console.assert(calculate_lrm_control_close("07:00", 1300, 1300, calculate_extended_limit(1300, 20000)) === "17:00 (+5)", "Test failed!") //Brasil 1300
    console.assert(calculate_lrm_control_close("07:00", 1200, 1200, calculate_extended_limit(1200, 15000)) === "05:30 (+4)", "Test failed!") //Tasmania
}