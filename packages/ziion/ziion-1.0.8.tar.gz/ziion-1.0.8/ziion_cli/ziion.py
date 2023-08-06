import subprocess


def self_update():
    print("updating ziion-cli...")
    print("\nCurrent version:")
    subprocess.run(["ziion", "--version"],
                   stderr=subprocess.STDOUT, check=False)
    print("\n")
    subprocess.run(["pipx", "upgrade", "ziion"],
                   stderr=subprocess.STDOUT, check=False)
    print("\nNew version:")
    subprocess.run(["ziion", "--version"],
                   stderr=subprocess.STDOUT, check=False)
