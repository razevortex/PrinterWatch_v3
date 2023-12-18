/*
for creating a table:
data strucs: 
keys (list of table column names): list(str,...)
obj : list(dict,...) *the dict has keys according to columns and its value is the actual entry

for creating groups:
keys as table
obj : list(dict{name: Groupname, obj: *table obj*}, ...)

both:
id : a id of html parent where the list/s should be  added

use:

createFlexboxList(id, keys, obj);

createFlexboxGroupedList(id, obj, keys);

*/

function addChildDiv(parent, class_, text, child_id){
	var parent = document.getElementById(parent);
    var child = document.createElement("div");
    if (text != ""){
    	child.innerHTML = "<p>"+text+"</p>";
    }
    child.setAttribute('class', class_);
    if (child_id != ""){
    	child.setAttribute('id', child_id);
    }
	parent.appendChild(child);
}

function createFlexboxList(parent_id, keys, obj){
    for (let i in keys){
	    let key = keys[i];
        addChildDiv(parent_id, "row theme-head", "", parent_id+"cols");
        addChildDiv(parent_id+"cols", "col", "", parent_id+key+"col");
        var heading = key.charAt(0).toUpperCase() + key.slice(1);
        addChildDiv(parent_id+key+"col", "theme theme-head", heading, "");
        for (let j in obj){
        	var item = obj[j];
            addChildDiv(parent_id+key+"col", "theme theme-body", item[key], "");
        }
    }
}

function createFlexboxGroupedList(parent_id, group_obj, keyList){
	for (let i in group_obj){
    	
    	let groupObj = group_obj[i];
        let groupId = groupObj.name;
        addChildDiv(parent_id, "list-main theme-mainbg", "", groupId);
        addChildDiv(groupId, "title theme-head theme-title", groupId, "");
        let Obj = groupObj.obj;
        createFlexboxList(groupId, keyList, Obj);
        addChildDiv(groupId, "end theme-head theme-title", " ", "");
    }

}

