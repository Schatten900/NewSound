function addFormPlaylist() {
   const form = document.getElementById("addFormMusicPlaylist");
   if (form.style.display === "none") {
      form.style.display = "block";
   }
   else {
      form.style.display = "none";
   }
}

function addMusicInMusicSaves(event) {
   event.preventDefault();
   const musicName = document.getElementById("musicaInput");
   const artistaName = document.getElementById("artistaInput");
   const musica = document.getElementById("fileUpload");

   //objeto FormData é um "json" permite enviar dados binarios como imagem/musica
   const formData = new FormData();
   formData.append("action", "add");

   if (musicName.value)
      formData.append("musicaName", musicName.value);

   if (artistaName.value)
      formData.append("artistaName", artistaName.value);

   if (musica.files.length > 0)
      formData.append("musica", musica.files[0]);

   let userUrl = `http://${window.location.host}/musicasSalvas`;
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

function addMusicInPlaylists(event,playlistId){
   event.preventDefault();
   const musicName = document.getElementById("musicaInput");
   const artistaName = document.getElementById("artistaInput");
   const musica = document.getElementById("fileUpload");

   //objeto FormData é um "json" permite enviar dados binarios como imagem/musica
   const formData = new FormData();
   formData.append("action", "add");

   if (musicName.value)
      formData.append("musicaName", musicName.value);

   if (artistaName.value)
      formData.append("artistaName", artistaName.value);

   if (musica.files.length > 0)
      formData.append("musica", musica.files[0]);

   let userUrl = `http://${window.location.host}/playlistUser/${playlistId}`;
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


//Funcao para mostrar o arquivo mp3 caso nao haja no banco de dados
function showMp3() {
   const inputFile = document.getElementById("showFile");
   if (inputFile.style.display === "none") {
      inputFile.style.display = "block";
   }
   else {
      inputFile.style.display = "none";
   }
}

