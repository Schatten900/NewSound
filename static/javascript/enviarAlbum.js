function enviarAlbum(event) {
    event.preventDefault();

    let codAlbum = event.currentTarget.getAttribute('data-album-cod');
    console.log(codAlbum)
    let artistaURL = `http://${window.location.host}/artista/${codAlbum}`;
    const messageArtista = {
        "action": "enviar",
        codAlbum: codAlbum
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