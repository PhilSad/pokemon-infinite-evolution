# pokemon-infinite-evolution

```bash
# dl image encoder

huggingface_cli login

export MODEL_DIR="stable-diffusion-v1-5/stable-diffusion-v1-5"
export OUTPUT_DIR="controlnet_pokemon"

accelerate launch train_controlnet.py \
 --pretrained_model_name_or_path=$MODEL_DIR \
 --controlnet_model_name_or_path=lllyasviel/control_v11e_sd15_ip2p \
 --image_column=evolution \
 --conditioning_image_column=origin \
 --caption_column=caption_basic \
 --output_dir=$OUTPUT_DIR \
 --dataset_name=PhilSad/pokemon_evolution_512 \
 --resolution=512 \
 --learning_rate=1e-5 \
 --validation_image "./val_images/mew.png" "./val_images/donphan.png" \
 --validation_prompt "Make this pokemon evolve" "Make this pokemon evolve" \
 --train_batch_size=4

```