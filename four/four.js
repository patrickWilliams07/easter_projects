class Item {
    static items = [];
    static fixedCost = 2000;
    constructor(name, price, variableCost){
        this.name = name;
        this.price = price;
        this.variableCost = variableCost;
        Item.items.push(this);
    }
    get quantity () {
        return Math.ceil(Item.fixedCost/(this.price-this.variableCost));
    }
}

function update() {
    while (document.getElementById("table-items").firstChild) {
        document.getElementById("table-items").removeChild( document.getElementById("table-items").firstChild);
    }
    for (let item of Item.items) {
        data = [item.name, item.price, item.variableCost, item.quantity]
        row = document.createElement("tr");
        document.getElementById("table-items").appendChild(row);
        for (let i = 0; i <= 3; i++) {
            row.appendChild(document.createElement("td"));
            row.lastChild.innerText = data[i];
        }
    }
}

document.getElementById("new-product").addEventListener("submit", function(event){
    event.preventDefault();
    new Item(document.getElementById("name").value, document.getElementById("price").value, document.getElementById("variable-cost").value);
    document.getElementById("name").value = ""
    document.getElementById("price").value = ""
    document.getElementById("variable-cost").value = ""
    update();
})

document.getElementById("fixed-cost-submit").onclick = function(){
    Item.fixedCost = document.getElementById("fixed-cost").value;
    document.getElementById("display-fixed-cost").innerText = `It is currently ${Item.fixedCost}`
    document.getElementById("fixed-cost").value = ""
    update();
}

document.getElementById("text-file").addEventListener("change", function(event){
    const reader = new FileReader();
    reader.readAsText(event.target.files[0], "UTF-8");
    reader.onload = function(event){
        let data = event.target.result.split("\r\n");
        for (let row of data){
            row = row.split(" ");
            new Item(row[0],row[1],row[2]);
        }
        update();
    }
}, false)

document.getElementById("reset").onclick = function(){
    if (confirm("Are you sure you want to reset?\nYou will lose all your data and cannot revert this action.")){
        Item.items = []
        update();
    }
}

window.addEventListener('beforeunload', (event) => {
    event.preventDefault();
    event.returnValue = '';
});