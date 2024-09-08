//Funcao para mostrar o form de adicionar musicas
function addFormPlaylist() {
    const form = document.getElementById("addFormMusicPlaylist");
    if (form.style.display === "none") {
        form.style.display = "block";
    }
    else {
        form.style.display = "none";
    }
}

//Funcao para redirecionar pra artista x
function enviarArtista(event) {
    event.preventDefault();
    let artistaURL = `http://${window.location.host}/artista`;

    let codArtista = event.currentTarget.getAttribute('data-artista-cod');
    const messageArtista = {
        "action": "enviar",
        codArtista: codArtista
    }

    fetch(artistaURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(messageArtista)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro aconteceu durante o envio:", reponse.message);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect;
            }
            else {
                console.log("Ocorreu um erro")
            }
        })
        .catch(error => console.error("Erro achado: ", error));
}

//Funcao visual para expandir musicas do album
function expandir() {
    const form = document.getElementById("formMusicContainer");
    console.log("10000");
    if (form.style.display === "none") {
        form.style.display = "block";
    }
    else {
        form.style.display = "none";
    }
    console.log("Bloqueou")
}