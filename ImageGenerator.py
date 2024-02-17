import replicate

# import os

# REPLICATE_API_TOKEN = "r8_cz4Ff15djoalYvr8hqX9tYIpiBXL98S0sgprF"
# os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def generate_image(prompt):
    print(f"Generating image for: {prompt}")
    img_url = replicate.run(
      "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
      input={"prompt": prompt}
    )

    print(img_url)
    return img_url
