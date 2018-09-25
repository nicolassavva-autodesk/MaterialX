#include "stdlib/sx-glsl/overlay.glsl"

void mx_overlay_color3(vec3 fg, vec3 bg, float mix, out vec3 result)
{
    result = mix * overlay(fg, bg) + (1-mix) * bg;
}
