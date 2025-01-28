function selecTodos() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = true;
  });
}
function validarForm() {
  const form = document.getElementById("myForm");
  const errorMessage = document.getElementById("errorMessage");
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const selects = [
      document.getElementById("microred"),
      document.getElementById("mes"),
      document.getElementById("anio"),
    ];

    let isValid = true;

    // Validar campos obligatorios (selects)
    selects.forEach((select) => {
      if (select.value === "") {
        select.classList.add("invalid");
        isValid = false;
      } else {
        select.classList.remove("invalid");
      }
    });

    // Validar checkboxes (nueva validación)
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    let isChecked = false;
    checkboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        isChecked = true;
      }
    });

    if (!isValid || !isChecked) {
      if (!isValid) {
        errorMessage.textContent =
          "Por favor, completa todos los campos en las Opciones de Filtro.";
        errorMessage.style.display = "block";
      } else if (!isChecked) {
        errorMessage.textContent =
          "Por favor, selecciona al menos un checkbox.";
        errorMessage.style.display = "block";
      }
      setTimeout(() => {
        errorMessage.style.display = "none";
      }, 6000);
    } else {
      errorMessage.style.display = "none";
      form.submit();
    }
  });
}
