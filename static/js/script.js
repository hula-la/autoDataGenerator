function submitForm() {
    console.log(JSON.stringify(jsonObject));

  
    var form = document.getElementById("data-generate");

    var formData = new FormData(form);
    var jsonObject = {};
  
    for (const [key, value]  of formData.entries()) {
      jsonObject[key] = value;
    }


    fetch('/table/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jsonObject)
    });
  }
