function attachToken(form, obj){
    for (const [key, value] of Object.entries(obj)) {
      	let temp = document.createElement("input");
      	temp.type = "hidden";
      	temp.name = key;
      	temp.value = value;
      	temp.form = form.id;
        form.appendChild(temp);
  }
}

