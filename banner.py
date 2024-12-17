from colorama import init, Fore

def banner():
    print(Fore.GREEN)
    print("""
▄• ▄▌.▄▄ ·  ▄▄·        ▄▄▄·▄▄▄ .
█▪██▌▐█ ▀. ▐█ ▌▪ ▄█▀▄ ▐█ ▄█▀▄.▀·
█▌▐█▌▄▀▀▀█▄██ ▄▄▐█▌.▐▌ ██▀·▐▀▀▪▄
▐█▄█▌▐█▄▪▐█▐███▌▐█▌.▐▌▐█▪·•▐█▄▄▌
 ▀▀▀  ▀▀▀▀ ·▀▀▀  ▀█▄▀▪.▀    ▀▀▀ 
""" + Fore.CYAN + f"Root user bypass tool ({Fore.WHITE}Tested on Kali Live USB{Fore.CYAN})" + Fore.RESET)
    print(Fore.YELLOW + "[ ! ] Physical access to the device is required, booting into Kali Live USB is recommended." + Fore.RESET)
