function salvarFicha(ficha) {
    const request = indexedDB.open("FichaDB", 1);

    request.onupgradeneeded = function (event) {
        const db = event.target.result;
        if (!db.objectStoreNames.contains("fichas")) {
            db.createObjectStore("fichas", { keyPath: "id" });
        }
    };

    request.onsuccess = function (event) {
        const db = event.target.result;
        const tx = db.transaction("fichas", "readwrite");
        const store = tx.objectStore("fichas");

        store.put(ficha);

        tx.oncomplete = () => console.log("Ficha salva no IndexedDB.");
    };
}

function atualizarCampo(id, caminho, novoValor) {
    const request = indexedDB.open("FichaDB", 1);

    request.onsuccess = function (event) {
        const db = event.target.result;
        const tx = db.transaction("fichas", "readwrite");
        const store = tx.objectStore("fichas");

        const getRequest = store.get(id);
        getRequest.onsuccess = function () {
            const ficha = getRequest.result;
            if (!ficha) return console.warn("Ficha não encontrada");

            const partes = caminho.split(".");
            let alvo = ficha;
            for (let i = 0; i < partes.length - 1; i++) {
                alvo = alvo[partes[i]];
            }
            alvo[partes.at(-1)] = novoValor;

            store.put(ficha);
            console.log(`Campo "${caminho}" atualizado com sucesso.`);
        };
    };
}

function obterFicha(id, callback) {
    const request = indexedDB.open("FichaDB", 1);

    request.onsuccess = function (event) {
        const db = event.target.result;
        const tx = db.transaction("fichas", "readonly");
        const store = tx.objectStore("fichas");

        const getRequest = store.get(id);
        getRequest.onsuccess = function () {
            const ficha = getRequest.result;
            if (callback) callback(ficha);
        };
    };
}


const ficha= {
    id: "ficha_001",
    nome_personagem: "",
    nome_jogador: "",
    pontos_de_vida: {
        atual: 0,
        maxima: 0,
        temporaria: 0
    },
    dado_de_vida: {
        info_dado: "",
        gasto: 0,
        maxima: 0
    },
    salvaguarda_contra_morte: {
        sucessos: [false, false, false],
        falhas: [false, false, false]
    },
    nivel: 0,
    xp: 0,
    antecedente: "",
    linhagem: "",
    classe: "",
    tencia: "",
    bonus_proficiencia: "",
    inspiracao_heroica: false,
    tamanho: "",
    iniciativa: 0,
    deslocamento: 0,
    instintos_passivos: {
        perpecao_passiva: 0,
        investigacao_passiva: 0,
        intuicao_passiva: 0
    },
    classe_armadura: {
        valor: 0,
        escudo: false
    },
    atributos: {
        forca: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false },
            atletismo: { valor: 0, check: false }
        },
        destreza: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false },
            acrobacia: { valor: 0, check: false },
            furtividade: { valor: 0, check: false },
            presdigitacao: { valor: 0, check: false }
        },
        constituicao: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false }
        },
        inteligencia: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false },
            arcanismo: { valor: 0, check: false },
            investigacao: { valor: 0, check: false },
            natureza: { valor: 0, check: false },
            religiao: { valor: 0, check: false }
        },
        sabedoria: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false },
            intuicao: { valor: 0, check: false },
            lidar_com_animais: { valor: 0, check: false },
            medicina: { valor: 0, check: false },
            percepcao: { valor: 0, check: false },
            sobrevivencia: { valor: 0, check: false }
        },
        carisma: {
            modificador: 0,
            valor: 0,
            salvaguarda: { valor: 0, check: false },
            atuacao: { valor: 0, check: false },
            enganacao: { valor: 0, check: false },
            intimidacao: { valor: 0, check: false },
            persuasao: { valor: 0, check: false }
        }
    },
    ataques: [
        { nome: "", modificador_de_acerto: 0, dano: "", tipo: "", observacao: "" },
        { nome: "", modificador_de_acerto: 0, dano: "", tipo: "", observacao: "" },
        { nome: "", modificador_de_acerto: 0, dano: "", tipo: "", observacao: "" }
    ],
    inventario: [
        { nome: "", quantidade: 0, peso: "", ativo: false, observacao: "" },
        { nome: "", quantidade: 0, peso: "", ativo: false, observacao: "" },
        { nome: "", quantidade: 0, peso: "", ativo: false, observacao: "" },
        { nome: "", quantidade: 0, peso: "", ativo: false, observacao: "" }
    ],
    treinamentos: [
        {
            armadura: {
                leve: false,
                medio: false,
                pesado: false,
                escudo: false
            },
            armas: [],
            ferramentas: []
        }
    ],
    idiomas: []
}

//salvarFicha(ficha)

obterFicha("ficha_001", (ficha) => {
    console.log("Ficha carregada:", ficha);
});

//atualizarCampo("ficha_001", "pontos_de_vida.atual", 15);

function salvarPrimeiraTela(){
    let nome_personagem = document.getElementById("nome_personagem").value
    let nome_jogador = document.getElementById("nome_jogador").value

    salvarFicha(ficha)

    atualizarCampo("ficha_001", "nome_personagem", nome_personagem)
    atualizarCampo("ficha_001", "nome_jogador", nome_jogador)

}