var updateID = null
var container = document.querySelector("#myContainer");
var welcomeContainer = document.querySelector("#welcomeContainer");
var registeredList = document.querySelector(".list");
var createButton = document.querySelector("#registerbutton");
var updateButton = document.querySelector("#updatebutton");
var updateForm = document.querySelector(".updateform");
var createForm = document.querySelector(".registerform");
var createaccountform = document.querySelector(".createaccountform");
var loginForm = document.querySelector(".loginform");
var addbutton = document.querySelector("#addbutton");
var signupbutton = document.querySelector("#signupbutton");
var createaccountbutton = document.querySelector("#createaccountbutton");
var loginbutton = document.querySelector("#loginbutton");

var showcreateAccount = function() {
  loginForm.style.display = 'none'
  createaccountform.style.display = 'block'
};

signupbutton.onclick = function() {
    showcreateAccount()

};


addbutton.onclick = function() {
    updateForm.style.display = "none"
    createForm.style.display = "block"
};


loginbutton.onclick = function() {
  var emailInput = document.querySelector('#loginemail');
  var email = encodeURIComponent(emailInput.value);
  var passwordInput = document.querySelector("#loginpassword")
  var password = encodeURIComponent(passwordInput.value);
  var dataString = "email=" + email + "&password=" + password;
  fetch("http://localhost:8080/sessions", {
    body: dataString,
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(function (response){
    if (response.status == 201) {
      showCreate()
      registeredList.style.display = "block"
      loginForm.style.display = 'none'
      createaccountform.style.display = 'none'
      createForm.style.display = 'block'
      container.innerHTML = "";
      loadCars();
      response.json().then(function (user) {
        console.log(user);

        var welcomeDiv = document.createElement('div');
        welcomeContainer.appendChild(welcomeDiv);

        var newItem = document.createElement('h3');
        var Welcome = document.createTextNode('Welcome ')
        newItem.appendChild(Welcome);
        welcomeDiv.appendChild(newItem)

        var firstName = document.createElement('h3');
        firstName.innerHTML = user.fname;
        welcomeDiv.appendChild(firstName);

        welcomeDiv.style.display = "inline"
      });
    }else if (response.status == 401) {
      alert("Email or Password not valid, try again")
    } else {
      alert("Unknown Error")
    }
  });
};

createaccountbutton.onclick = function() {
  var fnameInput = document.querySelector("#firstname");
  var fname = encodeURIComponent(fnameInput.value);
  var lnameInput = document.querySelector("#lastname");
  var lname = encodeURIComponent(lnameInput.value);
  var emailInput = document.querySelector("#email");
  var email = encodeURIComponent(emailInput.value);
  var passwordInput = document.querySelector('#password');
  var password = encodeURIComponent(passwordInput.value);

  var userdata = "fname=" + fname + "&lname=" + lname + "&email=" + email + "&password=" + password;
  fetch('http://localhost:8080/users', {
    body: userdata,
    method: "POST",
    credentials: 'include',
    headers: {
      'Content-Type':'application/x-www-form-urlencoded'
    }
  }).then(function(response){
    if (response.status == 201) {
      loginForm.style.display = "block"
      createaccountform.style.display = "none"
      alert("You have Successfully Registered")
    } else if (response.status == 422) {
       alert("Email is already in use, please try again")
    } else {
      alert("Unknown Error")
    }
  });
};

createButton.onclick = function() {
    var ownerNameInput = document.querySelector("#owner_name");
    var owner_name = encodeURIComponent(ownerNameInput.value);
    var yearInput = document.querySelector("#year");
    var year = encodeURIComponent(yearInput.value);
    var makeInput = document.querySelector("#make");
    var make = encodeURIComponent(makeInput.value);
    var modelInput = document.querySelector("#model");
    var model = encodeURIComponent(modelInput.value);
    var colorInput = document.querySelector("#color");
    var color = encodeURIComponent(colorInput.value);
    var platenumberInput = document.querySelector("#platenumber");
    var platenumber = encodeURIComponent(platenumberInput.value);

    var data = "owner_name=" + owner_name + "&year=" + year + "&make=" + make + "&model=" + model + "&color=" + color + "&platenumber=" + platenumber;
    fetch('http://localhost:8080/cars', {
        body: data,
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type':'application/x-www-form-urlencoded'
        }
    }).then(function (){
        container.innerHTML = "";
        loadCars();
    });
};


var deleteCar = function(id) {
    fetch('http://localhost:8080/cars/'+id, {
        credentials: 'include',
        method: 'DELETE'
    }).then(function (){
        container.innerHTML = "";
        loadCars();
    });
};




updateButton.onclick = function() {
    var ownerNameInput = document.querySelector("#updateowner_name");
    var owner_name = encodeURIComponent(ownerNameInput.value);
    var yearInput = document.querySelector("#updateyear");
    var year = encodeURIComponent(yearInput.value);
    var makeInput = document.querySelector("#updatemake");
    var make = encodeURIComponent(makeInput.value);
    var modelInput = document.querySelector("#updatemodel");
    var model = encodeURIComponent(modelInput.value);
    var colorInput = document.querySelector("#updatecolor");
    var color = encodeURIComponent(colorInput.value);
    var platenumberInput = document.querySelector("#updateplatenumber");
    var platenumber = encodeURIComponent(platenumberInput.value);

    var data = "owner_name=" + owner_name + "&year=" + year + "&make=" + make + "&model=" + model + "&color=" + color + "&platenumber=" + platenumber;
    fetch('http://localhost:8080/cars/'+ updateID, {
        body: data,
        credentials: 'include',
        method: 'PUT',
        headers: {
            'Content-Type':'application/x-www-form-urlencoded'
        }
    }).then(function (){
        container.innerHTML = "";
        loadCars();
    });
    showCreate()
};


var showCreate = function() {
  updateForm.style.display = 'none'
  createForm.style.display = 'block'
  createaccountform.style.display = 'none'
  loginForm.style.display = 'none'

};

var showUpdate = function(car) {
    updateID = car.id
    updateForm.style.display = "block"
    createForm.style.display = "none"
    var ownerNameInput = document.querySelector("#updateowner_name");
    ownerNameInput.value = car.owner_name
    var yearInput = document.querySelector("#updateyear");
    yearInput.value = car.year
    var makeInput = document.querySelector("#updatemake");
    makeInput.value = car.make
    var modelInput = document.querySelector("#updatemodel");
    modelInput.value = car.model
    var colorInput = document.querySelector("#updatecolor");
    colorInput.value = car.color
    var platenumberInput = document.querySelector("#updateplatenumber");
    platenumberInput.value = car.platenumber
};

var loadCars = function () {
    fetch ('http://localhost:8080/cars', {
        credentials: 'include'
    }).then(function (response) {
        if (response.status == 401) {
            loginForm.style.display = "block"
        } else if (response.status == 200) {
            createForm.style.display = 'block'
            registeredList.style.display = 'block'
            loginForm.style.display = "none"
        } else {
            alert("Unknown Error")
        };
        return response.json();
    }).then(function (cars) {
        console.log(cars)
        cars.forEach(function (car){
           var carDiv = document.createElement('div');
            container.appendChild(carDiv);

            var owner_nameItem = document.createElement('li');
            owner_nameItem.innerHTML = car.owner_name;
            carDiv.appendChild(owner_nameItem);

            var newItem = document.createElement('li');
            var textNode = document.createTextNode(' ');
            newItem.appendChild(textNode);
            carDiv.appendChild(newItem);

            var yearItem = document.createElement('li');
            yearItem.innerHTML = car.year;
            carDiv.appendChild(yearItem);

            var newItem = document.createElement('li');
            var textNode = document.createTextNode(' ');
            newItem.appendChild(textNode);
            carDiv.appendChild(newItem);

            var makeItem = document.createElement('li');
            makeItem.innerHTML = car.make;
            carDiv.appendChild(makeItem);

            var newItem = document.createElement('li');
            var textNode = document.createTextNode(' ');
            newItem.appendChild(textNode);
            carDiv.appendChild(newItem);

            var modelItem = document.createElement('li');
            modelItem.innerHTML = car.model;
            carDiv.appendChild(modelItem);

            var delButton = document.createElement('button');
            delButton.innerHTML = "Delete";
            delButton.onclick = function () {
                var choice = confirm("Delete this Registration?");
                if (choice == true) {
                    console.log("Registration Deleted: ", car);
                    deleteCar(car.id)
                } else {
                    console.log("Delete canceled for Registration: ", car);
                }
            };
            modelItem.appendChild(delButton);

            var updateButton = document.createElement('button');
            updateButton.innerHTML = "Edit";
            updateButton.onclick = function () {
                showUpdate(car)
                console.log("a registration was updated: ", car);
            };
            modelItem.appendChild(updateButton);

        });
    });
};

loadCars();
