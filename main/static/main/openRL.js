document.getElementById('balanceForm').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('add_balance.php', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            alert(data);
            closeModal('balanceModal');
        })
        .catch(error => console.error('Ошибка:', error));
};
// Открытие и закрытие модальных окон
function openModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Закрытие модального окна при клике на фон
window.onclick = function(event) {
    if (event.target.classList.contains('bg-black')) {
        closeModal('loginModal');
        closeModal('registerModal');
    }
};

// AJAX для формы входа с обновлением интерфейса
document.getElementById('loginForm').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('login.php', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            if (data.includes('успешно')) {
                // Скрыть модальное окно и обновить интерфейс
                closeModal('loginModal');
                document.getElementById('authButtons').classList.add('hidden');
                document.getElementById('profileMenu').classList.remove('hidden');
                document.getElementById('userEmailDisplay').innerText = formData.get('email');
            } else {
                document.getElementById('loginError').innerText = data;
                document.getElementById('loginError').classList.remove('hidden');
            }
        })
        .catch(error => console.error('Ошибка:', error));
};


// AJAX для формы регистрации
document.getElementById('registerForm').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('register.php', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            if (data.includes('успешно')) {
                alert('Регистрация успешна!');
                closeModal('registerModal');
            } else {
                document.getElementById('registerError').innerText = data;
                document.getElementById('registerError').classList.remove('hidden');
            }
        })
        .catch(error => console.error('Ошибка:', error));
};
document.addEventListener('DOMContentLoaded', function () {
    const userEmail = '<?php echo $_SESSION["user_email"] ?? ""; ?>';
    if (userEmail) {
        document.getElementById('authButtons').classList.add('hidden');
        document.getElementById('profileMenu').classList.remove('hidden');
        document.getElementById('userEmailDisplay').innerText = userEmail;
    } else {
        document.getElementById('authButtons').classList.remove('hidden');
        document.getElementById('profileMenu').classList.add('hidden');
    }
});

function selectPlan(planId, price) {
    const userEmail = '<?php echo $_SESSION["user_email"] ?? ""; ?>';
    if (!userEmail) {
        alert("Сначала авторизуйтесь, чтобы купить VPN-план.");
        openModal('loginModal');
    } else {
        openModal('balanceModal');
        document.getElementById('balanceAmount').value = price;
    }
}
