
var button = document.getElementById("button_submit");
var error = document.getElementById("error");
var toast = document.getElementById("toast");


button.addEventListener("click", function (event) {
    event.preventDefault(); // страница не перезагружается

    var name = document.getElementById("name").value;
    var problem = document.getElementById("problem").value;
    var description = document.getElementById("description").value;
    var adress = document.getElementById("adress").value;
    
    console.log("Имя:", name, "Проблема:", problem, "Описание:", description, "Адрес:", adress);

    // валидация: ищем первое незаполненное поле
    var empty = "";
    if (name === "") {
        empty = "Не заполнено поле: имя";
    } else if (problem === "") {
        empty = "Не заполнено поле: проблема";
    } else if (description === "") {
        empty = "Не заполнено поле: описание ситуации";
    }
    else if (adress.length < 5) {
        empty = "адрес должен быть не менее 5 символов";

    }
    
    if (empty !== "") {
        error.textContent =  empty;
        error.classList.remove("hidden");
        toast.classList.add("hidden");
        return; // дальше не идём, на сервер не отправляем
    }

    error.classList.add("hidden");

    // шлём на сервер те же данные, что отправил бы сам браузер
    fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
            name: name,
            problem: problem,
            description: description,
            adress: adress
            
        })
    })
        .then(function (response) {
            return response.text();
        })
        .then(function (text) {
            console.log("ответ сервера:", text);
            
            toast.classList.remove("hidden");
            toast.innerHTML = text;
            
            document.getElementById("name").value = "";
            document.getElementById("problem").value = "";
            document.getElementById("description").value = "";
            document.getElementById("adress").value = "";

            // таймер: через 5 секунд прячем сообщение обратно
            // setTimeout(function () {
            //     toast.classList.add("hidden");
            // }, 5000);
        })
        .catch(function (err) {
            error.textContent = "Не отправилось: " + err;
            error.classList.remove("hidden");
        });
            
});
