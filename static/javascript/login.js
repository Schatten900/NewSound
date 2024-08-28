function Login(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const senha = document.getElementById("loginPassword").value;

    if (!email || !senha) {
        window.alert("Preencha todos os dados corretamente.");
        return;
    }
    console.log(email)
    console.log(senha)

    let messageData = {
        email: email,
        senha: senha
    };

    let loginUrl = `http://${window.location.host}/login`
    fetch(loginUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(messageData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("HTTP ERROR: ", response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data === "success") {
                console.log("Houve um erro ao logar: ", data.message)
            }
            else {
                window.location.href = data.redirect;

            }
        })
        .catch(error => console.error("Erro ao buscar os dados do usuario: ", error));
}
