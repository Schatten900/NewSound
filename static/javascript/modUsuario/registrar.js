function Registrar(event) {
    event.preventDefault();
    const nome = document.getElementById("registerNome").value;
    const email = document.getElementById("registerEmail").value;
    const senha = document.getElementById("registerPassword").value;
    const confirm = document.getElementById("registerConfirm").value;

    if (senha !== confirm) {
        window.alert("As senhas devem ser iguais")
        return;
    }
    if (!nome || !email || !senha || !confirm) {
        window.alert("Preencha os dados corretamente")
        return;
    }

    let registerUrl = `http://${window.location.host}/register`
    messageData = {
        nome: nome,
        email: email,
        senha: senha,
    };

    fetch(registerUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(messageData)
    })
        .then(response => {
            if (!response.ok)
                throw new Error(`Http Erro:`, response.status)
            return response.json()
        })
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect
            }
            else {
                console.log("Houve um erro ao logar: ", data.message)
            }
        })
        .catch(error => console.error("Erro ao buscar os dados do usuario:", error));
}