#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct PointLight{
    vec3 position;
    
    vec3 Ia;
    vec3 Id;
    vec3 Is;

    float constant;
    float linear;
    float quadratic;
};

struct DirectionLight{
    vec3 direction;
    
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

struct SpotLight{
    vec3 position;
    vec3 direction;
    float cutoff;
    
    vec3 Ia;
    vec3 Id;
    vec3 Is;

    float constant;
    float linear;
    float quadratic;
};

uniform PointLight light;
uniform DirectionLight dirLight;
uniform SpotLight spotLight;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getPointLight(vec3 color,PointLight light){
    vec3 Normal = normalize(normal); 
    
    // ambient light
    vec3 ambient = light.Ia;

    // diffusion light
    vec3 lightDir = normalize(light.position-fragPos);
    float diff = max(0,dot(lightDir,Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir,Normal);
    float spec = pow(max(dot(viewDir, reflectDir),0),32);
    vec3 specular = spec * light.Is;

    // attenuation
    float lightDistance = length(light.position-fragPos);
    float att = 1.0/
    (
        light.constant +
        light.linear * lightDistance + 
        light.quadratic * lightDistance * lightDistance
    );

    return color * (ambient * att + diffuse * att + specular * att);
    
}

vec3 getDirectionLight(vec3 color,DirectionLight light){
    vec3 lightDir = normalize(-light.direction);
    vec3 Normal = normalize(normal); 
    
    // ambient light
    vec3 ambient = light.Ia;

    // diffusion light
    float diff = max(0,dot(lightDir,Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir,Normal);
    float spec = pow(max(dot(viewDir, reflectDir),0),32);
    vec3 specular = spec * light.Is;

    return color * ( ambient + diffuse + specular );
}

vec3 getSpotLight(vec3 color,SpotLight light){
    vec3 lightDir = normalize(light.position-fragPos);
    vec3 Normal = normalize(normal); 
    float theta = dot(lightDir,normalize(-light.direction));  
    if(theta > light.cutoff)
    {
        // ambient light
        vec3 ambient = light.Ia;

        // diffusion light
        float diff = max(0,dot(lightDir,Normal));
        vec3 diffuse = diff * light.Id;

        // specular light
        vec3 viewDir = normalize(camPos - fragPos);
        vec3 reflectDir = reflect(-lightDir,Normal);
        float spec = pow(max(dot(viewDir, reflectDir),0),32);
        vec3 specular = spec * light.Is;
		// attenuation
    	float lightDistance = length(light.position-fragPos);
    	float att = 1.0/
    	(
        	light.constant +
	        light.linear * lightDistance + 
    	    light.quadratic * lightDistance * lightDistance
    	);

    	return color * (ambient * att + diffuse * att + specular * att);
        
    }
    else
    {
        return vec3(0,0,0);
    }
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0,uv_0).rgb;
    color = pow(color,vec3(gamma));
    

    vec3 result = getDirectionLight(color,dirLight);
    result += getPointLight(color,light);
    result += getSpotLight(color,spotLight);

    color = pow(result,1/vec3(gamma));
    fragColor = vec4(color, 1.0);
}