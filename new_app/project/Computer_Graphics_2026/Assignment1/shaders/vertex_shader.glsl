#version 120

attribute vec3 vertexPosition;
attribute vec3 vertexColor;

varying vec3 fragmentColor;
uniform mat4 mvp;

void main() {
    fragmentColor = vertexColor;
    gl_Position = mvp * vec4(vertexPosition, 1.0);
}