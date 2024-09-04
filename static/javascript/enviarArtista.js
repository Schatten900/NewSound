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