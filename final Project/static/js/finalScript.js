  // Customer object
  class Customer {
    constructor(firstName, lastName, phone, address, city, state, zip) { 
        this.firstName = firstName;
        this.lastName = lastName;
        this.phone = phone;
        this.address = address;
        this.city = city;
        this.state = state;
        this.zip = zip;
    }
}

// Pizza object
class Pizza {
    constructor(size, toppings) {
        this.size = size;
        this.toppings = toppings;
    }

    getBasePrice() {
        const prices = {
            small: 8,
            medium: 10,
            large: 12
        };
        return prices[this.size];
    }

    getToppingPrice() {
        const toppingPrices = {
            cheese: 1,
            pepperoni: 2,
            mushrooms: 1.5,
            onions: 1,
            olives: 1.5,
            sausage: 2
        };
        return this.toppings.reduce((total, topping) => total + toppingPrices[topping], 0);
    }

    getTotalPrice() {
        return this.getBasePrice() + this.getToppingPrice();
    }
}


class Order {
    constructor(customer) {
        this.customer = customer;
        this.pizzas = [];
    }

    addPizza(pizza) {
        this.pizzas.push(pizza);
    }

    getOrderSummary() {
        let summary = `Customer Information:\nName: ${this.customer.firstName} ${this.customer.lastName}\nPhone: ${this.customer.phone}\nAddress: ${this.customer.address}\n`;
        this.pizzas.forEach((pizza, index) => {
            summary += `\nPizza ${index + 1} - Size: ${pizza.size}\nToppings: ${pizza.toppings.join(", ")}\nPrice: $${pizza.getTotalPrice().toFixed(2)}\n`;
        });
        return summary;
        }
    
        getTotalPrice() {
            let total = this.pizzas.reduce((sum, pizza) => sum + pizza.getTotalPrice(), 0);
            return total;
        }
    
        getTaxedTotal() {
            return this.getTotalPrice() * 1.10;
        }
}
let order = null;
let pizzaCount = 0;

// Add pizza form functionality
document.getElementById('add-pizza').addEventListener('click', () => {
    pizzaCount++;
    const pizzaContainer = document.getElementById('pizza-container');
    const pizzaDiv = document.createElement('div');
    pizzaDiv.classList.add('pizza');
    pizzaDiv.innerHTML = `
        <label for="pizza-size">Size:</label>
        <select class="pizza-size">
            <option value="small">Small ($8)</option>
            <option value="medium">Medium ($10)</option>
            <option value="large">Large ($12)</option>
        </select><br>
        <label>Toppings:</label><br>
        <input type="checkbox" class="topping" value="cheese"> Cheese ($1)<br>
        <input type="checkbox" class="topping" value="pepperoni"> Pepperoni ($2)<br>
        <input type="checkbox" class="topping" value="mushrooms"> Mushrooms ($1.5)<br>
        <input type="checkbox" class="topping" value="onions"> Onions ($1)<br>
        <input type="checkbox" class="topping" value="olives"> Olives ($1.5)<br>
        <input type="checkbox" class="topping" value="sausage"> Sausage ($2)<br>
    `;
    pizzaContainer.appendChild(pizzaDiv);

});

// Submit customer information
document.getElementById('customer-form').addEventListener('submit', (e) => {
    e.preventDefault();

    const customerFirstName = document.getElementById('firstName').value;
    const customerLastName = document.getElementById('lastName').value;
    const customerPhone = document.getElementById('customer-phone').value;
    const customerAddress = document.getElementById('address').value;
    const customerCity = document.getElementById('city').value;
    const customerState = document.getElementById('state').value;
    const customerZip = document.getElementById('zip').value;
    const customer = new Customer(customerFirstName, customerLastName, customerPhone, customerAddress, customerCity, customerState, customerZip); 
    order = new Order(customer);
    updateOrderSummary();
    alert("Customer information submitted.");
    document.getElementById('showDelCo').style = "display:block";
});

// Submit order
document.getElementById('pizza-form').addEventListener('submit', (e) => {
    e.preventDefault();

    if (!order) {
        alert("Please enter customer information first.");
        return;
    }

    const pizzaDivs = document.querySelectorAll('.pizza');
    pizzaDivs.forEach(pizzaDiv => {
        const size = pizzaDiv.querySelector('.pizza-size').value;
        const toppings = [];
        pizzaDiv.querySelectorAll('.topping:checked').forEach(topping => {
            toppings.push(topping.value);
        });

        const pizza = new Pizza(size, toppings);
        order.addPizza(pizza);
    });

// Display the order summary
updateOrderSummary();
    alert("Order submitted!");
});

// Function to update the order summary and total
function updateOrderSummary() {
    if (!order) return;

const summaryElement = document.getElementById('order-summary');
    summaryElement.innerHTML = order.getOrderSummary();

const totalElement = document.getElementById('total-price');
    totalElement.innerHTML = order.getTaxedTotal().toFixed(2);
}

//order be for Delivery
function chooseDelCo() {
    let ordDel = document.getElementById('del').selected;
    let ordCo = document.getElementById('Co').selected;

    if (ordDel) {
        document.getElementById('delInfo').style = "display:block";
        document.getElementById('coInfo').style = "display:none";
    }
    if (ordCo) {
        document.getElementById('delInfo').style = "display:none";
        document.getElementById('coInfo').style = "display:block";
    }
}
