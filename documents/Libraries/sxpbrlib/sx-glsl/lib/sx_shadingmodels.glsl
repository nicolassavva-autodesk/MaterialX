float sx_ggx_D(float cosTheta, float alpha)
{
    float alpha2 = alpha * alpha;
    float cosTheta2 = cosTheta * cosTheta;
    return alpha2 / (M_PI * sx_square(cosTheta2 * (alpha2 - 1.0) + 1.0));
}

float sx_smith_G1(float cosTheta, float alpha)
{
    float alpha2 = alpha * alpha;
    float cosTheta2 = cosTheta * cosTheta;
    return 2.0 / (1.0 + sqrt(1.0 + alpha2 * (1.0 - cosTheta2) / cosTheta2));
}

float sx_smith_G(float NdotL, float NdotV, float alpha)
{
    return sx_smith_G1(NdotL, alpha) * sx_smith_G1(NdotV, alpha);
}

float sx_fresnel_schlick_roughness(float cosTheta, float ior, float roughness)
{
    float F0 = (ior - 1.0) / (ior + 1.0);
    F0 *= F0;
    return F0 + (max(1.0 - roughness, F0) - F0) * pow(1.0 - cosTheta, 5.0);
}
