import subprocess


def block_ports():
    try:
        # Block incoming traffic on ports 1-1024
        subprocess.run(
            [
                "sudo",
                "iptables",
                "-A",
                "INPUT",
                "-p",
                "tcp",
                "--dport",
                "1:1024",
                "-j",
                "DROP",
            ],
            check=True,
        )
        subprocess.run(
            [
                "sudo",
                "iptables",
                "-A",
                "INPUT",
                "-p",
                "udp",
                "--dport",
                "1:1024",
                "-j",
                "DROP",
            ],
            check=True,
        )

        # Block outgoing traffic on ports 1-1024
        subprocess.run(
            [
                "sudo",
                "iptables",
                "-A",
                "OUTPUT",
                "-p",
                "tcp",
                "--dport",
                "1:1024",
                "-j",
                "DROP",
            ],
            check=True,
        )
        subprocess.run(
            [
                "sudo",
                "iptables",
                "-A",
                "OUTPUT",
                "-p",
                "udp",
                "--dport",
                "1:1024",
                "-j",
                "DROP",
            ],
            check=True,
        )

        print("Ports 1-1024 have been blocked.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while blocking ports: {e}")


def main():
    block_ports()


if __name__ == "__main__":
    main()
