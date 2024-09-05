//Funcao para acoes de musica (remover e favoritar ate entao)
function acoesMusicas(event, endpoint, acao) {
    event.preventDefault();

    let musicaCod = event.currentTarget.getAttribute('data-music-cod');
    const requestData = {
        action: acao,
        CodMusic: musicaCod
    };
    console.log(musicaCod)
    console.log(acao)

    let musicaURL = `http://${window.location.host}/${endpoint}`;

    fetch(musicaURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
        .then(response => {
            if (!response.ok)
                throw new Error("Erro ao executar ação", response.status);
            return response.json();
        })
        .then(data => {
            if (data.status !== "success") {
                console.log("Houve um erro na ação");
            }
            else {
                window.location.href = data.redirect;
            }
        })
        .catch(error => console.error("Erro achado: ", error));
}

