let navi = document.getElementById('navi')

let nav_icon = document.querySelectorAll("#navi .nav-item")

// trocar nav_icon active 
function navIconActive(){
    criancas = navi.children
    for (let i = 0; i < criancas.length; i++) {
        criancas[i].classList.remove('active')

        criancas[i].addEventListener('click', (e)=>{
            e.classList.add('active')
        })
      }
}
