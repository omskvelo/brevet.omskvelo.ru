rows = document.querySelectorAll(".collapsible")
btnExpand = document.querySelector("#btn-expand")
btnCollapse = document.querySelector("#btn-collapse")

btnExpand.addEventListener('click', function(e){
    rows.forEach(r => r.classList.remove('hidden'))
    btnExpand.setAttribute('hidden','')
    btnCollapse.removeAttribute('hidden')
}
)
btnCollapse.addEventListener('click', function(e){
        rows.forEach(r => r.classList.add('hidden'))
        btnCollapse.setAttribute('hidden','')
        btnExpand.removeAttribute('hidden')
    }
)

rows1 = document.querySelectorAll(".collapsible1")
btnExpand1 = document.querySelector("#btn-expand1")
btnCollapse1 = document.querySelector("#btn-collapse1")

btnExpand1.addEventListener('click', function(e){
    rows1.forEach(r => r.classList.remove('hidden'))
    btnExpand1.setAttribute('hidden','')
    btnCollapse1.removeAttribute('hidden')
}
)
btnCollapse1.addEventListener('click', function(e){
        rows1.forEach(r => r.classList.add('hidden'))
        btnCollapse1.setAttribute('hidden','')
        btnExpand1.removeAttribute('hidden')
    }
)

rows2 = document.querySelectorAll(".collapsible2")
btnExpand2 = document.querySelector("#btn-expand2")
btnCollapse2 = document.querySelector("#btn-collapse2")

btnExpand2.addEventListener('click', function(e){
    rows2.forEach(r => r.classList.remove('hidden'))
    btnExpand2.setAttribute('hidden','')
    btnCollapse2.removeAttribute('hidden')
}
)
btnCollapse2.addEventListener('click', function(e){
        rows2.forEach(r => r.classList.add('hidden'))
        btnCollapse2.setAttribute('hidden','')
        btnExpand2.removeAttribute('hidden')
    }
)
