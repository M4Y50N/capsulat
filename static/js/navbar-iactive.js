let navi = document.getElementById('navi')

let nav_icon = document.querySelectorAll("#navi .nav-item")

// trocar nav_icon active 
function navIconActive(){
    nav_icon.forEach(i => {
        i.classList.remove('active')
    });

    nav_icon.onclick 
}

navIconActive()
// nav_icon.addEventListener("click", navIconActive(nav_icon))