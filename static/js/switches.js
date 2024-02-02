function attachInput(form, obj){
  for (const [key, value] of Object.entries(obj)) {
  	
  	let box = document.getElementById(key);
    	let hiddenIn = document.createElement("input");
    	hiddenIn.type = "hidden";
    	hiddenIn.name = key;
	hiddenIn.form = form;
	hiddenIn.value = value;
	hiddenIn.id = key+"_state";
	box.className = "state"+value;
    	box.appendChild(hiddenIn);
  }
}

function switchDiv(div){
	let ele = document.getElementById(div.id+"_state");
    if (ele.value == "on"){
        ele.value = "off";
    }
    else {
    	ele.value = "on";
    }
	div.className = "state"+ele.val
}
