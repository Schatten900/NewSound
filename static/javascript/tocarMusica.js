function tocarMusica(event, endpoint) {
    event.preventDefault();
    let musicaCod = event.currentTarget.getAttribute('data-music-cod');

    const requestData = {
        action: "tocar",
        CodMusic: musicaCod
    };
    //Link dinamico, assim podemos usar essa funcao em todas as funcionalidades ate entao
    let musicaURL = `http://${window.location.host}/${endpoint}`;

    fetch(musicaURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
        //Espera-se o arquivo de audio do banco de dados recebidos pelo flask
        .then(response => response.blob())
        .then(blob => {
            const player = document.getElementById("playerMusica");
            //Cria um URL temporario que contem a musica
            const url = URL.createObjectURL(blob);
            //Vincula a url temporaria ao player de musica
            player.src = url;
            //Toca a musica em si
            player.load();
            player.play();
        })
        .catch(error => console.error('Erro ao tocar a música:', error));

}