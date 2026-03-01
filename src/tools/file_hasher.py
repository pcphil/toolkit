import hashlib
import os


class FileHasher:

    SUPPORTED_ALGORITHMS = ("md5", "sha1", "sha256", "sha512")

    @staticmethod
    def hash_file(input_path, algorithm="sha256", output_path=None):
        """Compute the hex digest of a file using the specified algorithm."""
        if algorithm not in FileHasher.SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Unsupported algorithm '{algorithm}'. "
                f"Choose from: {', '.join(FileHasher.SUPPORTED_ALGORITHMS)}"
            )

        h = hashlib.new(algorithm)
        with open(input_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)

        digest = h.hexdigest()

        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"{digest}  {os.path.basename(input_path)}\n")
            print(f"Hash written to '{output_path}'")

        print(f"{algorithm}: {digest}")
        return digest

    @staticmethod
    def verify_hash(input_path, expected_hash, algorithm="sha256"):
        """Verify a file's hash against an expected hex digest. Returns True/False."""
        actual = FileHasher.hash_file(input_path, algorithm=algorithm)
        match = actual.lower() == expected_hash.lower()
        print(f"{'Match' if match else 'MISMATCH'}: expected {expected_hash}, got {actual}")
        return match
