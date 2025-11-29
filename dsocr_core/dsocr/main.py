from dsocr.cli import parse_args, run_cli


def main():
    args = parse_args()
    try:
        out = run_cli(args.input, args.api_key, args.prompt, args.output, args.output_dir, args.ext, args.debug)
        print(f"Saved OCR result to: {out}")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
