{
    let targetTextBlock = document.querySelector('.insert-copy-btn')
    let splitPattern = /(.*)(\d{16}|\d{4}\s\d{4}\s\d{4}\s\d{4})(.*)/
    targetTextBlock.innerHTML = targetTextBlock.innerText.replace(splitPattern, "$1 <a>$2</a> $3")
    targetTextBlock.classList.remove('insert-copy-btn')
    let cardLink = targetTextBlock.querySelector('a')
    cardLink.setAttribute('class', 'btn btn-light btn-card-copy')

    cardLink.addEventListener('click', function(event) {
        navigator.clipboard.writeText(cardLink.innerText).then(
            () => {document.showNotification("Скопировано в буфер обмена")},
            () => {document.showNotification("Невозможно скопировать в буфер обмена")}
        )
    });



}