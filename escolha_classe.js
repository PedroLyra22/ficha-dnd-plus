const inputBusca = document.getElementById('busca-classe');
const selectOpcoes = document.getElementById('opcoes-classe');


const todasOpcoes = Array.from(selectOpcoes.options).map(op => op.text);

inputBusca.addEventListener('input', () => {
    const filtro = inputBusca.value.toLowerCase();
    selectOpcoes.innerHTML = '';

    todasOpcoes.forEach(texto => {
        if (texto.toLowerCase().includes(filtro)) {
            const opcao = document.createElement('option');
            opcao.text = texto;
            selectOpcoes.appendChild(opcao);
        }
    });
});