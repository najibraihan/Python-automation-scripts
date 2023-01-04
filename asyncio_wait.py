async def start_sniffing_and_capturing_traffic(file_path: str, device_id: str):
    lockdown = LockdownClient(serial=device_id)
    with open(file_path, 'wb') as fo:
        PcapdService.write_to_pcap(fo, PcapdService(lockdown=lockdown).watch())


def main() -> None:
    """Run local instance of network sniffer."""

    def _configure_logging(log_level: int = logging.INFO) -> None:
        """Configure console logging.
        Args:
            log_level: Log level.
        Returns:
            None.
        """
        root = logging.getLogger()
        root.setLevel(log_level)
        root.addHandler(rich_logging.RichHandler(rich_tracebacks=True))

    _configure_logging()

    parser = argparse.ArgumentParser(
        description="Run network sniffer on target device for determined time."
    )
    parser.add_argument(
        "--device-id", type=str, required=True, help="The ID of the device."
    )
    parser.add_argument(
        "--pcp-file", type=str, required=True, help="The name of pcap file."
    )
    parser.add_argument(
        "--duration", type=int, required=True, help="The duration."
    )

    args = parser.parse_args()

    device_id: str = args.device_id
    duration: int = args.duration
    pcap_file: str = args.pcap_file

    # create task
    task = asyncio.create_task(start_sniffing_and_capturing_traffic(device_id=device_id, file_path=pcap_file))

    # run function for the given duration
    try:
        asyncio.run(asyncio.wait_for(task, duration))
    except asyncio.TimeoutError:
        task.cancel()


if __name__ == '__main__':
    main()
