document.getElementById('scan-form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('overlay').style.display = 'flex';
});

/**
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Connexion réussie');
});

document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Inscription réussie');
});


let loginForm = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = () =>{
    loginForm.classList.toggle('active');
    searchForm.classList.remove('active');
    navbar.classList.remove('active');
}

**/