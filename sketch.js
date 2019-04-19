var bird;
let pipes = [];

function setup() {
  createCanvas(800, 600);
  bird = new Bird();
  pipes.push(new Pipe());
}

function keyPressed() {
  if (keyCode === ENTER) {
    bird.up();

  }
}

function draw() {






  background(0);
  if (frameCount % 40 == 0) {
    pipes.push(new Pipe());
  }
  bird.show();
  bird.update();
  for (var i = 0; i < pipes.length; i++) {
    pipes[i].show();
    pipes[i].update();
    if (pipes[i].hit(bird)) {
      background(220,0,0);

    }
    if (pipes[i].offscreen()) {
  pipes.splice(i, 1);
    }


    }
  }
