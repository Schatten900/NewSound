function editUser(event) {
    event.preventDefault();
    const formUser = document.getElementById("containerUsuarioActions");
    const formEdit = document.getElementById("formEditConta");

    if (formEdit.style.display === "block") {
        formEdit.style.display = "none";
        formUser.style.height = "520px";
    }
    else {
        formEdit.style.display = "block";
        formUser.style.height = "600px";
    }
}

function SaveEditUser(event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileUpload");
    const nomeInput = document.getElementById("nameEdit");
    const emailInput = document.getElementById("emailEdit");

    //objeto FormData é um "json" permite enviar dados binarios como imagem
    const formData = new FormData();
    formData.append("action", "edit");

    if (nomeInput.value)
        formData.append("nome", nomeInput.value);

    if (emailInput.value)
        formData.append("email", emailInput.value);

    if (fileInput.files.length > 0)
        formData.append("imagem", fileInput.files[0]);

    let userUrl = `http://${window.location.host}/usuario`;
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

function Redirecionar(event,endpoint,acao){
    event.preventDefault();
    let userUrl = `http://${window.location.host}/${endpoint}`;
    const formData = new FormData()
    formData.append("action",acao);
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