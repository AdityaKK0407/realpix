import os, shutil

DATA_FAKE_VALID = r'd:\realpix\data\valid\fake'
os.makedirs(DATA_FAKE_VALID, exist_ok=True)

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}

def copy_images(src_dir, prefix):
    count = 0
    for f in os.listdir(src_dir):
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
            src = os.path.join(src_dir, f)
            dst = os.path.join(DATA_FAKE_VALID, prefix + f)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                count += 1
    return count

n1 = copy_images(r'd:\realpix\MidJourney\valid', 'mj_')
print('MidJourney valid copied:', n1)

n2 = copy_images(r'd:\realpix\StableDiffusion\valid', 'sd_')
print('StableDiffusion valid copied:', n2)

print('Total valid/fake:', len(os.listdir(DATA_FAKE_VALID)))
print('Done!')
