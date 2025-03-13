file_path = "test_utils.py"

try:
    # Read file and check for null bytes
    with open(file_path, "rb") as f:
        data = f.read()

    # If null bytes are found, remove them
    if b"\x00" in data:
        cleaned_data = data.replace(b"\x00", b"")

        with open(file_path, "wb") as f:
            f.write(cleaned_data)

        print(f"✅ Null bytes removed from {file_path}")
    else:
        print(f"⚡ No null bytes found in {file_path}")

except FileNotFoundError:
    print(f"❌ Error: {file_path} not found.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
