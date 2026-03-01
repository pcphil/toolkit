import csv
import json
import os

import yaml


class DataConverter:

    @staticmethod
    def _get_unique_path(path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    @staticmethod
    def csv_to_json(input_path, output_path="output/converted.json"):
        """Read a CSV file and write it as a JSON array."""
        with open(input_path, "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(rows)} records to '{output_path}'")
        return output_path

    @staticmethod
    def json_to_csv(input_path, output_path="output/converted.csv"):
        """Read a JSON array and write it as CSV."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("JSON file must contain a non-empty array of objects")

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Saved {len(data)} records to '{output_path}'")
        return output_path

    @staticmethod
    def json_to_yaml(input_path, output_path="output/converted.yaml"):
        """Read a JSON file and write it as YAML."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        print(f"Saved to '{output_path}'")
        return output_path

    @staticmethod
    def yaml_to_json(input_path, output_path="output/converted.json"):
        """Read a YAML file and write it as JSON."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved to '{output_path}'")
        return output_path

    @staticmethod
    def csv_to_yaml(input_path, output_path="output/converted.yaml"):
        """Read a CSV file and write it as YAML (via JSON intermediate)."""
        with open(input_path, "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(rows, f, default_flow_style=False, allow_unicode=True)

        print(f"Saved {len(rows)} records to '{output_path}'")
        return output_path

    @staticmethod
    def yaml_to_csv(input_path, output_path="output/converted.csv"):
        """Read a YAML file (expected array of objects) and write it as CSV."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("YAML file must contain a non-empty array of objects")

        output_path = DataConverter._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Saved {len(data)} records to '{output_path}'")
        return output_path
