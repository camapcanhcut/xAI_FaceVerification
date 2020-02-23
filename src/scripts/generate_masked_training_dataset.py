import os
import argparse
import numpy as np
from glob import glob
from PIL import Image
from tqdm import tqdm


def apply_mask(img_dir, mask_dir, out_dir, csv_path):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    csv_content = []
    print(f'>>> Img_dir[0]:{img_dir[0]}')
    print(f'>>> mask_dir[0]:{mask_dir[0]}')
    print(f'>>> out_dir:{out_dir}')
    print(f'>>> csv_path:{csv_path}')
    for i, image_file in tqdm(enumerate(img_dir), total=len(img_dir)):
        mask_file = np.random.choice(mask_dir)
        image = Image.open(image_file)
        mask = Image.open(mask_file)
        masked = np.array(image) * np.expand_dims(np.array(mask), 2)

        name = os.path.basename(image_file)
        out_subdir = os.path.basename(os.path.dirname(image_file))
        if not os.path.exists(os.path.join(out_dir, out_subdir)):
            os.makedirs(os.path.join(out_dir, out_subdir))
        out_file = os.path.join(out_dir, out_subdir, name)
        Image.fromarray(masked).save(out_file)

        mask_number = os.path.join(os.path.basename(os.path.dirname(mask_file)), os.path.basename(mask_file))
        output_name = os.path.join(os.path.basename(out_dir), out_subdir, name)
        csv_content.append((output_name, mask_number))
    with open(csv_path, 'w') as filehandle:
        for listitem in csv_content:
            filehandle.write(f'{listitem[0]},{listitem[1]}\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--mask_ratio',
        type=int,
        default=25
    )
    parser.add_argument(
        '-md', '--mask_dir',
        type=str,
        default='../../datasets/face/masks'
    )
    parser.add_argument(
        '-id', '--image_dir',
        type=str,
        default='../../datasets/face/faces_emore/imgs'
    )
    parser.add_argument(
        '-od', '--output_dir',
        type=str,
        default='../../datasets/face/masked_ms1m'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    ratio = args.mask_ratio
    mask_dir = glob(os.path.join(args.mask_dir, f'{ratio}/*'))
    img_dir = glob(os.path.join(args.image_dir, '**/*.jpg'))
    out_dir = os.path.join(args.output_dir, f'imgs_masked{ratio}')
    csv_path = out_dir + '.csv'
    # print(img_dir)
    print(len(img_dir))
    np.random.seed(9487)
    apply_mask(img_dir, mask_dir, out_dir, csv_path)
