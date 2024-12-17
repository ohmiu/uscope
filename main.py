#!/usr/bin/env python3
from banner import banner
from utils import check_requirements, scan_disks, check_start, print_blue, get_credetionals, main_work


if __name__ == "__main__":
    banner()
    input("\nTap <ENTER> to continue...")
    check_start()
    check_requirements()
    work_partition = scan_disks()
    login, password = get_credetionals()
    print_blue("A hack of the target internal file system is underway. Please wait.")
    main_work(work_partition, login, password)
    