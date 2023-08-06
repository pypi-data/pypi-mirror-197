from nwebclient import sdb

def gen(pipe, prompt='photo', negative_prompt = None, prefix='sd',  guidance_scale = 7.5, num_inference_steps=30, height=800, width=640, num_images=1, dbfile='data.db'):
    # https://huggingface.co/docs/diffusers/v0.14.0/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline.__call__
    images = pipe(
      prompt,
      height = 800,
      width = 640,
      num_inference_steps = num_inference_steps,      # higher better quali default=45
      guidance_scale = guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
      num_images_per_prompt = num_images,
      negative_prompt = negative_prompt,
      ).images
    for i in range(len(images)):
        #  images[i].save(prefix+str(i)+".jpg")
        sdb.sdb_write_pil(images[i], prompt, negative_prompt, guidance_scale, prefix, dbfile)

