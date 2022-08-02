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
