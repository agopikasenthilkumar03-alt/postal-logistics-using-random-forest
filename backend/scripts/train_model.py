import argparse

from app.ml.random_forest import load_or_train_model


def main():
    parser = argparse.ArgumentParser(description="Train the Random Forest delay prediction model")
    parser.add_argument("--data", required=True, help="Path to training CSV data")
    args = parser.parse_args()

    model = load_or_train_model(args.data)
    print(f"Model trained and saved: {model.model_version}")


if __name__ == "__main__":
    main()
