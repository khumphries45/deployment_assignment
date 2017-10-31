var updateID = null
var container = document.querySelector("#myContainer");
var createButton = document.querySelector("#button");
var updateButton = document.querySelector("#updatebutton");
var updateForm = document.querySelector(".updateform");
var createForm = document.querySelector(".registerform");
var addbutton = document.querySelector("#addbutton");

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

var showCreate = function() {
    updateForm.style.display = "none"
    createForm.style.display = "block"
};

addbutton.onclick = function() {
    updateForm.style.display = "none"
    createForm.style.display = "block"
};

var loadCars = function () {
    fetch ('http://localhost:8080/cars').then(function (response) {
        return response.json();
    }).then(function (cars) {
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
