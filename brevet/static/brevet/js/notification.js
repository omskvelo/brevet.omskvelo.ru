document.showNotification = function(message){
    const notificationDom = document.querySelector('.notification')
    notificationDom.innerText = message
    notificationDom.style.opacity = 1
    setTimeout(()=>{notificationDom.style.opacity = 0}, 2500)
}
