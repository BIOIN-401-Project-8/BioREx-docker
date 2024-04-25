import argparse
import subprocess
import os
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../src/dataset_format_converter"))
from src.dataset_format_converter.convert_pubtator_2_tsv import main as convert_pubtator_2_tsv


def main():
    parser = argparse.ArgumentParser(description='run BioREx')
    parser.add_argument(
        'in_pubtator_file', help="input pubtator file"
    )
    parser.add_argument(
        'out_pubtator_file', help="output pubtator file"
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

    print('Converting the dataset into BioREx input format')


    convert_pubtator_2_tsv([
        "--exp_option", "biored_pred",
        "--in_pubtator_file", args.in_pubtator_file,
        "--out_tsv_file", args.out_tsv_file
    ])


    print('Generating RE predictions')
    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_visible_devices
    subprocess.run([
        "python", "src/run_ncbi_rel_exp.py",
        "--task_name", "biorex",
        "--test_file", args.out_tsv_file,
        "--use_balanced_neg", "false",
        "--to_add_tag_as_special_token", "true",
        "--model_name_or_path", args.pre_train_model,
        "--output_dir", "biorex_model",
        "--num_train_epochs", "10",
        "--per_device_train_batch_size", "16",
        "--per_device_eval_batch_size", "32",
        "--do_predict",
        "--logging_steps", "10",
        "--evaluation_strategy", "steps",
        "--save_steps", "10",
        "--overwrite_output_dir",
        "--max_seq_length", "512"
    ])

    subprocess.run([
        "cp", "biorex_model/test_results.tsv", "out_biorex_results.tsv"
    ])

    subprocess.run([
        "python", "src/utils/run_pubtator_eval.py",
        "--exp_option", "to_pubtator",
        "--in_test_pubtator_file", args.in_pubtator_file,
        "--in_test_tsv_file", args.out_tsv_file,
        "--in_pred_tsv_file", "out_biorex_results.tsv",
        "--out_pred_pubtator_file", args.out_pubtator_file
    ])


if __name__ == "__main__":
    main()
