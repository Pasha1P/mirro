// Навигация между страницами
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// Показ модальных окон
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Обработчики закрытия модальных окон
document.querySelectorAll('.close-modal').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
        closeBtn.closest('.modal').style.display = 'none';
    });
});

document.getElementById('create-board-btn').addEventListener('click', () => {
    showModal('create-board-modal');
});

// Закрытие модального окна при клике вне его содержимого
window.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// Переключение инструментов
document.querySelectorAll('.tool-btn').forEach(tool => {
    tool.addEventListener('click', () => {
        document.querySelectorAll('.tool-btn').forEach(t => t.classList.remove('active'));
        tool.classList.add('active');
        // Здесь можно добавить логику выбора инструмента
    });
});