document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('dados.json');
        const dados = await response.json();

        const opcoes = {
            classe: dados.classes.map(c => c.nome),
            raca: dados.racas.map(r => r.nome),
            nivel: Array.from({ length: 20 }, (_, i) => `${i + 1}`),
            antecedente: dados.antecedentes || []
        };

        Object.entries(opcoes).forEach(([campo, valores]) => {
            const select = document.querySelector(`select[name="${campo}"]`);
            if (select) {
                valores.forEach(valor => {
                    const option = document.createElement('option');
                    option.value = valor;
                    option.textContent = valor;
                    select.appendChild(option);
                });
            }
        });

    } catch (error) {
        console.error('Erro ao carregar dados.json:', error);
    }
});
