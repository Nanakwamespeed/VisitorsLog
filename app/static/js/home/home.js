document.getElementById('proceed-button').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission

    document.getElementById('loader').style.display = 'block';

    let request_reason = '';
    if(document.getElementById('selected-option').value.trim() === 'Specify') {
        request_reason = document.getElementById('specify-reason').value.trim();
    } else {
    request_reason = document.getElementById('selected-option').value.trim();
    }

//    console.log("THIS IS THE THE REASON: ", request_reason);

    // Collect form data
    const fullName = document.getElementById('full-name').value.trim();
    const contactMethod = document.querySelector('input[name="contact-method"]:checked').value;
    const contact = document.getElementById('contact').value.trim();
    const staff = document.getElementById('staff').value.trim();
    const reason = request_reason;
    const multiple = document.getElementById('multiple').checked;
    const counterValue = document.getElementById('counter').textContent.trim();
    let imagePath = ''; // Default to an empty string

    // Remove previous error indications
    document.querySelectorAll('.input-error').forEach(element => {
        element.classList.remove('input-error');
    });

    // Perform validations
    let hasError = false;
    let isValid = true;

    // Perform validations
    if (!fullName) {
        document.getElementById('full-name').classList.add('input-error');
        hasError = true;
        isValid = false;
        document.getElementById('loader').style.display = 'none';
//        alert('Full name is required.');
//        return;
    }
    if (!contactMethod) {
        document.querySelectorAll('input[name="contact-method"]').forEach(element => {
            element.classList.add('input-error');
        });
        hasError = true;
        isValid = false;
        document.getElementById('loader').style.display = 'none';
    } else {
        if (contactMethod === 'email' && !validateEmail(contact)) {
            document.getElementById('contact').classList.add('input-error');
            hasError = true;
            isValid = false;
            document.getElementById('loader').style.display = 'none';
        } else if (contactMethod === 'phone' && !validatePhoneNumber(contact)) {
            document.getElementById('contact').classList.add('input-error');
            hasError = true;
            isValid = false;
            document.getElementById('loader').style.display = 'none';
        }
    }

    if (!contact) {
        document.getElementById('contact').classList.add('input-error');
        hasError = true;
        isValid = false;
        document.getElementById('loader').style.display = 'none';
    }

    if (!staff) {
        document.getElementById('staff').classList.add('input-error');
        hasError = true;
        isValid = false;
        document.getElementById('loader').style.display = 'none';
    }

    if(!reason){
        document.getElementById('specify-reason').classList.add('input-error');
        hasError = true;
        isValid = false;
        document.getElementById('loader').style.display = 'none';
    }

    if(multiple) {
        if (counterValue < 2){
             alert('Number of visitors should be more than one.');
             document.getElementById('loader').style.display = 'none';
            return;
        }
    }

    if(!pictureCaptured){
         alert('Take a picture.');
         document.getElementById('loader').style.display = 'none';
         return;
    }


if (isValid) {
    // Capture image if one was taken
    if (pictureCaptured) {
        const canvas = document.getElementById('canvas');
        const imageData = canvas.toDataURL('image/png');

        // Send image to the server
        fetch('/upload-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            if (data.imagePath) {
                imagePath = data.imagePath; // Get the returned image path

                // Prepare data to be sent
                var formData = {
                    full_name: fullName,
                    contact_method: contactMethod,
                    contact: contact,
                    staff_name: staff,
                    reason: reason,
                    multiple_visitors: multiple,
                    number_of_visitors: counterValue,
                    image: imagePath // Include the image path
                };

                // Send AJAX request
                fetch('/create-visit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    // Handle response
//                    console.log('Success:', data);
                    document.getElementById('loader').style.display = 'none';
                    alert('Visit request submitted');
                    resetFormFields();
                    showStep("step-thankyou");
//                    window.location.reload();
                    // Optionally, you can redirect to another page or show a success message
                    // window.location.href = '/next-page';
                })
                .catch(error => {
                    document.getElementById('loader').style.display = 'none';
                    console.error('Error:', error);
                    alert('There was an error. Please try again.');
                });
            } else {
                alert('Error uploading image. Please try again.');
            }
        })
        .catch(error => {
            document.getElementById('loader').style.display = 'none';
            console.error('Error uploading image:', error);
            alert('Error uploading image. Please try again.');
        });
    } else {
        // Prepare data to be sent without image
        var formData = {
            full_name: fullName,
            contact_method: contactMethod,
            contact: contact,
            staff_name: staff,
            reason: reason,
            multiple_visitors: multiple,
            number_of_visitors: counterValue
        };

        // Send AJAX request
        fetch('/create-visit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Handle response
//            console.log('Success:', data);
            document.getElementById('loader').style.display = 'none';
            alert('Visit request submitted');
            resetFormFields();
            showStep("step-thankyou");
//            window.location.reload();
            // Optionally, you can redirect to another page or show a success message
            // window.location.href = '/next-page';
        })
        .catch(error => {
            document.getElementById('loader').style.display = 'none';
            console.error('Error:', error);
            alert('There was an error. Please try again.');
        });
    }
} else {
return;
}
});

// Validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhoneNumber(phone) {
    const re = /^[0-9]{10}$/; // Basic validation for a 10-digit phone number
    return re.test(phone);
}

document.getElementById('cancel-button').addEventListener('click', function(event) {
    // Display a confirmation dialog
    const userConfirmed = confirm('Are you sure you want to cancel? All changes will be lost.');

    if (userConfirmed) {
        // Clear all input fields and reset form controls
        document.getElementById('full-name').value = '';
        document.querySelector('input[name="contact-method"][value="email"]').checked = true; // Reset to default
        document.getElementById('contact').value = '';
        document.getElementById('staff').value = '';
        document.getElementById('multiple').checked = false;
        document.getElementById('counter').textContent = '2';
        // If the user confirms, reload the page
        window.location.reload(); // Reload the page
    } else {
        // If the user cancels, do nothing
        event.preventDefault();
    }
});

const translations = {
  en: {
    touch: "Complete your visit sign up in a few  simple steps",
    getStarted: "Get Started ",
    title: "What brings you here today?",
    back: "back",
    visit:"Visit Employee",
    delivery:"Package Delivery",
    appointment:"Appointment",
    service:"Provide Service",
    tour:"Facility Tour",
    specify:"Specify",
    fullname:"Fullname",
    phone:"Phone Number",
    staff:"Staff",
    multiple:"We are multiple individuals",
    picture:"Take a picture",
    capture:"Capture",
    submit:"Submit",
    cancel:"Cancel"
  },
  fr: {
    touch: "Complétez votre inscription à la visite en quelques étapes simples",
    getStarted: "Commencer",
    title: "Qu'est ce qui t'amène aujourd'hui?",
    back: "dos",
    visit:"Visiter un employé",
    delivery:"Livraison de colis",
    appointment:"Rendez-vous",
    service:"Rendre service",
    tour:"Visite d'entreprise",
    specify:"Spécifier",
    fullname:"Nom et prénom",
    phone:"Numéro de téléphone",
    staff:"Personnelle",
    multiple:"Nous sommes plusieurs individus",
    picture:"Prendre une photo",
    capture:"Capturer",
    submit:"Soumettre",
    cancel:"Annuler"
  },
  es: {
    touch: "Complete el registro de su recorrido en unos sencillos pasos.",
    getStarted: "Empezar",
    title: "¿Que te trae aquí hoy?",
    back: "atrás",
    visit:"Visita Empleado",
    delivery:"Entrega de paquetes",
    appointment:"Cita",
    service:"Proporcionar servicio",
    tour:"Tour de instalaciones",
    specify:"Especificar",
  }
};

function changeLanguage(language) {
  document.getElementById("touch").textContent = translations[language].touch;
  document.getElementById("getStarted").textContent = translations[language].getStarted;
  document.getElementById("title").textContent = translations[language].title;
  document.getElementById("back").textContent = translations[language].back;
  document.getElementById("back2").textContent = translations[language].back;
  document.getElementById("visit").textContent = translations[language].visit;
  document.getElementById("delivery").textContent = translations[language].delivery;
  document.getElementById("appointment").textContent = translations[language].appointment;
  document.getElementById("service").textContent = translations[language].service;
  document.getElementById("tour").textContent = translations[language].tour;
  document.getElementById("specify").textContent = translations[language].specify;
  document.getElementById("your-name").textContent = translations[language].fullname;
  document.getElementById("phone").textContent = translations[language].phone;
  document.getElementById("employee").textContent = translations[language].staff;
  document.getElementById("many").textContent = translations[language].multiple;
  document.getElementById("proceed-button").textContent = translations[language].submit;
  document.getElementById("cancel-button").textContent = translations[language].cancel;
  document.getElementById("picture").textContent = translations[language].picture;
  document.getElementById("capture-button").textContent = translations[language].capture;
}

function toggleDropdown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function selectOption(text, imgPath, lang) {
  var button = document.getElementById("dropdownButton");
  button.innerHTML = '<img src="' + imgPath + '" alt="' + text + '">' + text;
  changeLanguage(lang);
  toggleDropdown();
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn') && !event.target.matches('.dropbtn *')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
  function showStep(stepId) {
    document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));
    document.getElementById(stepId).classList.add('active');
  }

 function handleOptionClick(stepId, element) {
    // Set the value of the hidden field
    const optionText = element.getAttribute('data-option');
    document.getElementById('selected-option').value = optionText;
    document.getElementById('form-title').textContent = optionText;

    // Show or hide the Reason input based on the selected option
    if (optionText === 'Specify') {
        document.getElementById('reason-group').style.display = 'block';
        document.getElementById('specify-reason').setAttribute('required', 'true');
    } else {
        document.getElementById('reason-group').style.display = 'none';
        document.getElementById('specify-reason').removeAttribute('required');
    }

    // Show the selected step
    showStep(stepId);
}

  // Character counter for reason textarea
  const reasonInput = document.getElementById('reason');
  const charCount = document.getElementById('char-count');


  // Webcam capture functionality
  const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
let pictureCaptured = false;

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
    })
    .catch(err => {
        console.error("Error accessing the camera: " + err);
    });

captureButton.addEventListener('click', () => {
    if (captureButton.textContent === 'Capture') {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        video.style.display = 'none';
        canvas.style.display = 'block';
        captureButton.textContent = 'Recapture';
        captureButton.style.backgroundColor = 'grey';
        pictureCaptured = true;
    } else {
        video.style.display = 'block';
        canvas.style.display = 'none';
        captureButton.textContent = 'Capture';
        captureButton.style.backgroundColor = 'black';
        pictureCaptured = false;
    }
});

  // Counter for multiple individuals
  const counterDisplay = document.getElementById('counter');
  const increaseButton = document.getElementById('increase');
  const decreaseButton = document.getElementById('decrease');
  const counterContainer = document.getElementById('counter-container');
  const multipleCheckbox = document.getElementById('multiple');
  let counter = 2;

  increaseButton.addEventListener('click', () => {
      counter++;
      counterDisplay.textContent = counter;
  });

  decreaseButton.addEventListener('click', () => {
      if (counter > 2) {
          counter--;
          counterDisplay.textContent = counter;
      }
  });

  multipleCheckbox.addEventListener('change', () => {
      if (multipleCheckbox.checked) {
          counterContainer.style.display = 'flex';
      } else {
          counterContainer.style.display = 'none';
      }
  });

  // Change placeholder based on contact method
  const contactInput = document.getElementById('contact');
  const contactMethods = document.getElementsByName('contact-method');

  contactMethods.forEach(method => {
      method.addEventListener('change', () => {
          contactInput.placeholder = method.value === 'email' ? 'johndoe@gmail.com' : '123-456-7890';
      });
  });

  // Staff dropdown functionality
  document.addEventListener('DOMContentLoaded', () => {
    const staffInput = document.getElementById('staff');
    const staffList = document.getElementById('staff-list');

    staffInput.addEventListener('input', filterStaff);

    staffList.addEventListener('click', (event) => {
        if (event.target && event.target.classList.contains('dropdown-item')) {
            staffInput.value = event.target.textContent;
            staffList.style.display = 'none'; // Hide the dropdown after selection
        }
    });

    function filterStaff() {
        const search = staffInput.value.toLowerCase();

        if (search.length >= 2) {
            fetch(`/suggest-usernames?q=${search}`)
                .then(response => response.json())
                .then(data => {
                    staffList.innerHTML = '';

                    if (data.length > 0) {
                        data.forEach(name => {
                            const item = document.createElement('div');
                            item.classList.add('dropdown-item');
                            item.textContent = name;
                            staffList.appendChild(item);
                        });
                        staffList.style.display = 'block';
                    } else {
                        const item = document.createElement('div');
                        item.classList.add('dropdown-item');
                        item.textContent = 'No staff by that name';
                        staffList.appendChild(item);
                        staffList.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error fetching staff names:', error);
                });
        } else {
            staffList.style.display = 'none';
        }
    }

    // Hide the staff list when clicking outside
    document.addEventListener('click', (event) => {
        if (!staffInput.contains(event.target) && !staffList.contains(event.target)) {
            staffList.style.display = 'none';
        }
    });
});

function resetFormFields() {
    // Clear the text fields
    document.getElementById('full-name').value = '';
    document.getElementById('contact').value = '';
    document.getElementById('staff').value = '';

    // Reset the counter
    document.getElementById('counter').textContent = '2';

    // Reset the checkbox
    document.getElementById('multiple').checked = false;

    // Clear the captured image (if any)
    pictureCaptured = false;
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
}

document.addEventListener('DOMContentLoaded', function () {
    // Select the "thank you" section
    var thankYouSection = document.getElementById('step-thankyou');

    if (thankYouSection) {
        // Create an intersection observer
        var observer = new IntersectionObserver(function (entries) {
            // Check if the "thank you" section is visible
            if (entries[0].isIntersecting) {
                // Display the countdown text
<!--                document.getElementById('countdownDisplay').style.display = 'block';-->

                // Set initial countdown time
                var countdownElement = document.getElementById('countdown');
                var countdownTime = 5; // in seconds
                countdownElement.textContent = countdownTime + 's';

                // Update the countdown every second
                var interval = setInterval(function () {
                    countdownTime--;
                    countdownElement.textContent = countdownTime + 's';

                    if (countdownTime <= 0) {
                        clearInterval(interval); // Clear the interval
                        window.location.reload(); // Reload the page
                    }
                }, 1000); // Update every 1 second

                // Stop observing once it's visible
                observer.disconnect();
            }
        }, {
            threshold: 0.5 // Trigger when 50% of the element is visible
        });

        // Start observing the "thank you" section
        observer.observe(thankYouSection);
    }
});