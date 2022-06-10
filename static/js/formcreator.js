
function createSubmitObject(submitObj){
	let formObj = document.getElementById(submitObj.formId);
    let container = document.createElement('div');
        container.className = 'inputs';
  	    container.style.width = submitObj.width;
        container.style.height = submitObj.height;
        container.style.float = 'right';
  	formObj.appendChild(container);
	let sub = document.createElement('input');
	    sub.form = submitObj.formId;
  	    sub.type = 'submit';
        sub.className = 'submit';
        sub.value = submitObj.subText;
    container.appendChild(sub);
    }

function createHiddenObject(hiddenObj){
	let formObj = document.getElementById(hiddenObj.formId);
	let hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.form = hiddenObj.formId;
        hiddenInput.name = hiddenObj.inName;
        hiddenInput.id = hiddenObj.inId;
        hiddenInput.value = hiddenObj.inValue;
    formObj.appendChild(hiddenInput);
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
  	    inLabel.for = inputObj.inId;
        inLabel.className = inputObj.inLabelClass;
  	    inLabel.innerHTML = inputObj.inLabelText;
    container.appendChild(inLabel);
	let input = document.createElement('input');
	    input.form = inputObj.formId;
	    input.name = inputObj.inName;
  	    input.type = 'text';
        input.id = inputObj.inName;
        input.className = inputObj.inClass;
        input.value = inputObj.inValue;
	container.appendChild(input);
    }

function createForm(formObj){
	let site = document.getElementById('formContainer');
  	let formCont = document.createElement('div');
    	formCont.id = formObj.divId;
        formCont.className = formObj.divClass;
    site.appendChild(formCont);
    let form = document.createElement('form');
      	form.action = formObj.link;
        form.id = 'inputForm';
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


function detailDatasheet(datasheetObj){
	let container = document.createElement('div');
  	container.className = 'datasheet';
  	container.id = 'datasheetDiv';
  	let headdata = document.createElement('p');
  		headdata.className = 'datasheetHead';
  		headdata.innerHTML = datasheetObj.fixed[0] + ' / ' + datasheetObj.fixed[1];
  	container.appendChild(headdata);
	document.body.appendChild(container);
  	let formcontainer = document.createElement('form');
      	formcontainer.action = datasheetObj.formAction;
        formcontainer.id = datasheetObj.formId;
  container.appendChild(formcontainer);
				formcontainer.appendChild(oRideLine('deviceId', datasheetObj.editable.deviceId[0], datasheetObj.editable.deviceId[1], datasheetObj.access));
  			formcontainer.appendChild(oRideLine('location', datasheetObj.editable.location[0], datasheetObj.editable.location[1], datasheetObj.access));
  			formcontainer.appendChild(oRideLine('contact', datasheetObj.editable.contact[0], datasheetObj.editable.contact[1], datasheetObj.access));
  			formcontainer.appendChild(oRideLine('notes', datasheetObj.editable.notes[0], datasheetObj.editable.notes[1], datasheetObj.access));
				formcontainer.appendChild(createCheck(datasheetObj.access));
}



function createCheck(access){
let cont = document.createElement('div');
  	cont.className = 'inputs';
  	cont.setAttribute('display', 'flex');
		cont.setAttribute('flex-direction', 'row');
  let label = document.createElement('label');
    label.setAttribute('for', 'access_check');
  	label.innerHTML = 'accessable';
  cont.appendChild(label);
	let default_radio = document.createElement('input');
  	default_radio.type = 'hidden';
  	default_radio.name = 'access';
  	default_radio.value = 'false';
  cont.appendChild(default_radio);
  let radio = document.createElement('input');
  	radio.id = 'access_check';
  	radio.type = 'checkbox';
  	radio.name = 'access';
  	radio.value = 'true';
    if (access == 'true'){
    radio.checked = access;}
	cont.appendChild(radio);
  let sub = document.createElement('input');
  	sub.type = 'submit';
    sub.className = 'submit';
    sub.value = '>>';
    cont.appendChild(sub);
  return cont;

  }


function oRideLine(lineId, og, or, access){
	let cont = document.createElement('div');
  cont.className = 'inputs';
  cont.setAttribute('display', 'flex');
	cont.setAttribute('flex-direction', 'row');

  let label = document.createElement('label');
  label.setAttribute('for', lineId);
  label.className = 'details';
  label.innerHTML = og;
  cont.appendChild(label);
  let inputField = document.createElement('input');
  inputField.type = 'text';

  inputField.className = 'text';
  inputField.form = 'detailOr';
  inputField.id = lineId;
  inputField.name = lineId;

  inputField.value = or;
  cont.appendChild(inputField);
	return cont;
}
