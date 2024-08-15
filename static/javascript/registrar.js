function Registrar() {
    const nome = document.getElementById("registerNome").value;
    const email = document.getElementById("registerEmail").value;
    const senha = document.getElementById("registerPassword").value;
    const confirm = document.getElementById("registerConfirm").value;

    if (senha != confirm) {
        window.alert("As senhas devem ser iguais")
        return;
    }
    if (!nome || !email || !senha || !confirm) {
        window.alert("Preencha os dados corretamente")
        return;
    }

    let registerUrl = `https://${window.location.host}/register`
    messageData = {
        nome: nome,
        email: email,
        senha: senha,
        confirm: confirm
    }

    fetch(registerUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(messageData)
    })
        .then(response => {
            if (!response.ok)
                throw new Error(`Http Erro:${response.status}`)
            return response.json()
        })
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect
            }
            else {
                window.alert("Alguns dos dados podem estar incorretos")
            }
        })
        .catch(error => console.error("erro: ", error));
}