
function createSubmitObject(submitObj){
	let formObj = document.getElementById(submitObj.formId);
  let container = document.createElement('div');
    container.className = 'inputs';
  	container.style.width = submitObj.width;
    container.style.height = submitObj.height;
    container.style.float = 'right';
  	formObj.appendChild(container);
	let sub = document.createElement('input');
  	sub.type = 'submit';
    sub.className = 'submit';
    sub.value = submitObj.subText;
    container.appendChild(sub);
}

function createHiddenObject(hiddenObj){
		let formObj = document.getElementById(hiddenObj.formId);
			let input = document.createElement('input');
      input.type = 'hidden';
      input.name = hiddenObj.name;
      input.id = hiddenObj.name;
      input.value = hiddenObj.value;
}

function createSelectObject(selObj){
	let formObj = document.getElementById(selObj.formId);
  let container = document.createElement('div');
    container.className = 'inputs';
  	container.style.width = selObj.width;
  	formObj.appendChild(container);
  let selLabel = document.createElement('label');
  	selLabel.for = selObj.selId;
    selLabel.className = selObj.selLabelClass;
  	selLabel.innerHTML = selObj.selLabelText;
    	container.appendChild(selLabel);
  let sel = document.createElement('select');
  	sel.id = selObj.selId;
    sel.className = selObj.selClass;
    sel.name = selObj.selName;
    	container.appendChild(sel);
      for (var opt of selObj.selOptions){
      	var selOpt = document.createElement('option');
        	selOpt.value = opt;
          selOpt.innerHTML = opt;
        		sel.appendChild(selOpt);
      }
}

function createTextObject(inputObj){
	let formObj = document.getElementById(inputObj.formId);
  let container = document.createElement('div');
 	  container.className = 'inputs';
  	container.style.width = inputObj.width;
  	formObj.appendChild(container);
  let inLabel = document.createElement('label');
  	inLabel.for = inputObj.selId;
    inLabel.className = inputObj.inLabelClass;
  	inLabel.innerHTML = inputObj.inLabelText;
    	container.appendChild(inLabel);
	let input = document.createElement('input');
	input.name = inputObj.inName;
  	input.type = 'text';
    input.id = inputObj.inId;
    input.className = inputObj.inClass;
    input.value = inputObj.inValue;
			container.appendChild(input);
}

function createForm(formObj){
	let site = document.getElementById('content');
  	let formCont = document.createElement('div');
    	formCont.id = formObj.divId;
      formCont.className = formObj.divClass;
      	site.appendChild(formCont);
      let form = document.createElement('form');
      	form.action = formObj.link;
        form.id = formObj.formId;
        	formCont.appendChild(form);
      	for (var obj of formObj.inputs){
        	if (obj.objType == 'select'){
          	createSelectObject(obj.objData);
          }
          else if (obj.objType == 'input'){
          	createTextObject(obj.objData);
          }
          else if (obj.objType == 'hidden'){
          	createHiddenObject(obj.objData);
          }
          else if (obj.objType == 'submit'){
          	createSubmitObject(obj.objData);
          }
        }
}

