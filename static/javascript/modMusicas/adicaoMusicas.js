//Funcao para adicionar musica no banco de dados
function addMusicInMusic(event) {
   event.preventDefault();
   const musicName = document.getElementById("musicaInput");
   const artistaName = document.getElementById("artistaInput");
   const musica = document.getElementById("fileUpload");

   console.log(musicName.value)
   console.log(artistaName.value)

   //objeto FormData é um "json" permite enviar dados binarios como imagem/musica
   const formData = new FormData();
   formData.append("action", "add");

   if (musicName.value)
      formData.append("musicaName", musicName.value);

   if (artistaName.value)
      formData.append("artistaName", artistaName.value);

   if (musica.files.length > 0){
      formData.append("musica", musica.files[0]);
      console.log("aaaaaaaaaaaaaaaaaaaa")
   }
      

   let userUrl = `http://${window.location.host}/navegar`;
   fetch(userUrl, {
      method: "POST",
      body: formData
   })
      .then(response => {
         if (!response.ok) {
            throw new Error("HTTP ERROR: " + response.status);
         }
         return response.json();
      })
      .then(data => {
         if (data.status === "success") {
            window.location.href = data.redirect;
         }
         else {
            console.log("Houve um erro: ", data.message)
         }
      })
      .catch(error => {
         console.error("Erro ao editar o usuario", error);
      })
}


//Funcao para adicionar a musica em favoritos ou em playlist
function addMusicUser(event, endpoint) {
   event.preventDefault();
   let addUrl = `http://${window.location.host}/${endpoint}`;

   const musicName = document.getElementById("musicaInput").value;
   const artistaName = document.getElementById("artistaInput").value;
   console.log(musicName.value);
   console.log(artistaName.value);

   const infoAdd = {
      action: "add",
      musicName: musicName,
      artistaName: artistaName
   }

   fetch(addUrl, {
      method: "POST",
      headers: {
         "Content-Type": "application/json"
      },
      body: JSON.stringify(infoAdd)
   })
      .then(response => {
         if (!response.ok)
            throw new Error("Erro ao executar a response:", response.status)
         return response.json();
      })
      .then(data => {
         if (data.status !== "success") {
            window.console("Ocorreu um erro inesperado")
            window.alert("Musica nao encontrada")
         }
         else
            window.location.href = data.redirect;
      })
      .catch(error => console.error("Ocorreu um erro chamado: ", error))
}
