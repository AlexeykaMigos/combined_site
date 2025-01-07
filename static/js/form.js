async function submitForm(event) {
    event.preventDefault();

    const form = event.target; // Получаем форму
    const formData = new FormData(form); // Создаём объект FormData для сбора данных

    // Преобразуем FormData в JSON
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/reserve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message); 
        } else {
            const error = await response.json();
            alert(`Ошибка: ${error.detail}`);
        }
    } catch (err) {
        alert(`Ошибка отправки данных: ${err.message}`);
    }
}
