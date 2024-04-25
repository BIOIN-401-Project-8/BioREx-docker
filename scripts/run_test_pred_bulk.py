import argparse
import subprocess
import os
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description='run BioREx')
    parser.add_argument(
        'in_pubtator_dir', help="input pubtator directory"
    )
    parser.add_argument(
        'out_pubtator_dir', help="output pubtator directory"
    )
    parser.add_argument(
        '--out_tsv_file', help="output tsv file", default="out_processed.tsv"
    )
    parser.add_argument(
        '--pre_train_model', help="pretrained model", default="pretrained_model_biolinkbert"
    )
    parser.add_argument(
        '--cuda_visible_devices', help="cuda visible devices", default="0"
    )
    args = parser.parse_args()

    for infile in tqdm(os.listdir(args.in_pubtator_dir)):
        outfile = args.out_pubtator_dir + '/' + infile
        infile = args.in_pubtator_dir + '/' + infile
        if os.path.isfile(outfile):
            continue

        subprocess.run([
            "python", "scripts/run_test_pred.py",
            infile,
            outfile
        ])


if __name__ == "__main__":
    main()
