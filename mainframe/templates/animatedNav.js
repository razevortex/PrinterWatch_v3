
let grid = new Object();
let timer = new Object();

function init() {
  let grid = new Object;
  grid.pageSize = [window.innerWidth, window.innerHeight];
  grid.aPercent = [Math.ceil(grid.pageSize[0] / 100),
    Math.ceil(grid.pageSize[1] / 100)
  ];
  grid.contSizeExpand = [grid.aPercent[0] * 10, window.innerHeight];
  grid.contSizeCollapsed = [grid.aPercent[0] * 2, grid.aPercent[0] * 2];
  grid.logoSize = [grid.contSizeExpand[0], Math.ceil(grid.contSizeExpand[0] / 2)];
  grid.buttonWidth = grid.contSizeExpand[0];
  grid.buttonSlidePos = [grid.aPercent[0] * 2,
    (grid.contSizeExpand[0] - grid.aPercent[0] * 2)
  ];
grid.buttonTopSpacing = Math.ceil(window.innerHeight / 23);
  createContainer(grid);
  this.grid = grid;
}

window.onload = init();

function createContainer(g) {
  let grid = g;
  /* creating of the collapsable nav container */
  let element = document.createElement("div");
  element.collapsed = false;
  element.timer = null;
  element.id = 'container';
  element.style.width = grid.contSizeCollapsed[0] + 'px';
  element.style.height = grid.contSizeCollapsed[0] + 'px';
  document.getElementsByTagName('body')[0].appendChild(element); // appending it to body

  /* creating the logo image */

  var logo = document.createElement("img");
  logo.src = 'pw_logo_ghostly.png';
  logo.style.width = grid.logoSize[0] + 'px';
  logo.style.height = grid.logoSize[1] + 'px';
  logo.style.left = '0px';
  logo.style.top = '0px';
  document.getElementById('container').appendChild(logo); // appending it to the nav container

  /* creating the nav links as sliding buttons in a for loop */

  let btns = ['Monitor', 'Analytics'] // the ids / labels of the buttons that are going to created
  // will need another list or a combination with id list for the href links
  let timer = new Object;
  let top_pos;
  for (let i = 0; i < btns.length; i++) {
    var button = document.createElement("button");
	var spacing = i + 1
	spacing = spacing * grid.buttonTopSpacing;
    top_pos = grid.logoSize[1] + spacing;
    button.id = btns[i];
    timer[button.id] = null;
    button.style.width = grid.buttonWidth + 'px';
    button.style.left = grid.buttonSlidePos[1] + 'px';
    button.style.top = top_pos + 'px';
    button.innerHTML = btns[i];
    document.getElementById('container').appendChild(button); // appending the buttons to the container
  }
  this.timer = timer;
}



function clickEvent(_this) {
  _this.collapsed = !_this.collapsed;
  let target;
  let size = [parseInt(_this.style.width), parseInt(_this.style.height)];
  if (_this.collapsed == true) {
    target = this.grid.contSizeExpand;
  } else {
    target = this.grid.contSizeCollapsed;
  }
  clearInterval(_this.timer);
  _this.timer = null;
  _this.timer = setInterval(animate, 10);

  function animate() {

    if (size[0] == target[0] && size[1] == target[1]) {
      clearInterval(_this.timer);
      _this.timer = null;
    }
    if (_this.collapsed == true) {
      for (var i = 0; i < size.length; i++) {
        _this.style.background = 'rgba(13, 13, 13, 0.9)';
        size[i] += Math.ceil((target[i] - size[i]) / 25);
        if (size[i] > target[i]) {
          size[i] = target[i];
        }
        _this.style.width = size[0] + 'px';
        _this.style.height = size[1] + 'px';
      }
    } else if (_this.collapsed == false) {
      for (var i = 0; i < size.length; i++) {
        _this.style.background = 'rgba(13, 13, 13, 0.2)';
        size[i] -= Math.ceil((size[i] - target[i]) / 25);
        if (size[i] < target[i]) {
          size[i] = target[i];
        }
        _this.style.width = size[0] + 'px';
        _this.style.height = size[1] + 'px';
      }
    }
  }
}


function hoverSlider(elemId, eve) {
  // INIT portion to prepair the animation
  let elem = document.getElementById(elemId.id);

  console.log(elem);
  clearInterval(this.timer[elemId.id]); // stop timer of the triggering element
  this.timer[elemId.id] = null;
  let rect = elem.getBoundingClientRect(); // find the current position of element
  let pos = rect.left;
  // RUN timer the element with animation function according to the trigger event
  if (eve == 'mouseout') {
    this.timer[elemId.id] = setInterval(animate_in, 5);

    function animate_in() {
      pos+=2;
      elem.style.left = pos + "px";
      if (pos > this.grid.buttonSlidePos[1]) {
        elem.style.left = this.grid.buttonSlidePos[1] + "px";
        clearInterval(this.timer[elemId.id]);
      }
    }
  } else if (eve == 'mouseover') {

    this.timer[elemId.id] = setInterval(animate_out, 5);

    function animate_out() {
      pos-=2;
      elem.style.left = pos + "px";
      if (pos < this.grid.buttonSlidePos[0]) {
        elem.style.left = this.grid.buttonSlidePos[0] + "px";
        clearInterval(this.timer[elemId.id]);
      }
    }
  }
}


function foo() {
  let _this = document.getElementById('container');
  _this.addEventListener('click', function() {
    clickEvent(_this);
  }, false);
}

function foo2() {
  let btns = document.getElementsByTagName('button');


  for (var i = 0; i < btns.length; i++) {
    let ele = document.getElementById(btns[i].id);
    console.log(ele.timer);
    ele.addEventListener('mouseover', function() {
      hoverSlider(ele, 'mouseover');
    });
    ele.addEventListener('mouseout', function() {
      hoverSlider(ele, 'mouseout');
    });

  }
}

foo();
foo2();