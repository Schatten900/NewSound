function Login(event){
    event.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const senha = document.getElementById("loginPassword").value;

    if (!email || !senha){
        window.alert("Preencha todos os dados corretamente.");
        return;
    }
    let messageData = {
        email:email,
        senha:senha
    };
    loginUrl = `http://${window.location.host}/login`
    fetch(loginUrl,{
        method:"POST",
        headers:{
            "Content-Type:":"application/json"
        },
        body: JSON.stringify(messageData)
    })
    .then(response=>{
        if (!response.ok){
            throw new Error("HTTP ERROR: ", response.status); 
        }
        return response.json;
    })
    .then(data=>{
        if (data === "success"){
            window.location.href = data.redirect;
        }
        else{
            window.alert("Não foi possivel conectar a conta.")
            console.log("Houve um erro ao logar: ", data.message)
        }
    })
    .catch(error => console.error("Erro ao buscar os dados do usuario: ",error));
}
