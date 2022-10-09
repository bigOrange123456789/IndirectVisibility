attribute vec3 aVert;
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform vec4 uColor;
varying vec4 vCol;

void main() {
  // option #1 - fails
  gl_Position = uPMatrix * uMVMatrix * vec4(aVert, 1.0); 
  // option #2 - works
  gl_Position = vec4(aVert, 1.0); 
  // set color
  vCol = vec4(uColor.rgb, 1.0);
}