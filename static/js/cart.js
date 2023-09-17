document.addEventListener("DOMContentLoaded", () => {
  // your code here


const addToCartButtons = document.querySelectorAll(".add-to-cart");



addToCartButtons.forEach(button => {
  button.addEventListener("click", event => {
    const productName = button.dataset.name;
    const productPrice = parseFloat(button.dataset.price);
    console.log(productName);
    const cartRow = document.createElement("tr");
    cartRow.innerHTML = `
      <td>${productName}</td>
      <td>$${productPrice.toFixed(2)}</td>
      <td><input type="number" value="1" min="1"></td>
      <td>$${productPrice.toFixed(2)}</td>
      <td><button class="remove">Remove</button></td>
    `;
    const cartTable = document.querySelector(".cart tbody");
    cartTable.appendChild(cartRow);

    updateCartTotal();
  });
});



// Remove item from cart
const removeButtons = document.querySelectorAll(".remove");
removeButtons.forEach(button => {
  button.addEventListener("click", event => {
    event.target.parentElement.parentElement.remove();
    updateCartTotal();
  });
});

// Update cart total
function updateCartTotal() {
  const cartRows = document.querySelectorAll(".cart tbody tr");
  let subtotal = 0;
  cartRows.forEach(row => {
    const price = parseFloat(row.querySelector("td:nth-of-type(2)").textContent.replace("$", ""));
    const quantity = parseInt(row.querySelector("td:nth-of-type(3) input").value);
    const total = price * quantity;
    row.querySelector("td:nth-of-type(4)").textContent = "$" + total.toFixed(2);
    subtotal += total;
    console.log(subtotal);
  });
  const tax = subtotal * 0.1; // 10% tax
  const total = subtotal + tax;
  document.querySelector(".cart tfoot tr:nth-of-type(1) td:nth-of-type(2)").textContent = "$" + subtotal.toFixed(2);
  document.querySelector(".cart tfoot tr:nth-of-type(2) td:nth-of-type(2)").textContent = "$" + tax.toFixed(2);
  document.querySelector(".cart tfoot tr:nth-of-type(3) td:nth-of-type(2)").textContent = "$" + total.toFixed(2);
}

// Update cart total on quantity change
const quantityInputs = document.querySelectorAll(".cart input[type='number']");
quantityInputs.forEach(input => {
  input.addEventListener("change", () => {
    updateCartTotal();
  });
});

// Checkout button click
const checkoutButton = document.querySelector(".checkout");
checkoutButton.addEventListener("click", () => {
  alert("Thank you for your purchase!");
  const cartRows = document.querySelectorAll(".cart tbody tr");
  cartRows.forEach(row => {
    row.remove();
  });
  updateCartTotal();
});

});