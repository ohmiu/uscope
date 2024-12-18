import animation
import sys
import os
import subprocess
from colorama import Fore, init
from uuid import uuid4

init()

d_anim = ('In progress - ', 'iN progress / ', 'in Progress | ', 'in pRogress \\ ', 'in pgOgress - ', 'in proGress / ', 'in progRess | ', 'in progrEss \\ ', 'in progreSs - ', 'in progresS / ', 'in progress | ', 'in progress \\ ')

def check_sudo():
    if os.geteuid() != 0:
        return False
    else:
        return True

def cmd_check(command):
    command = command.split(" ")
    try:
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def next_step(callbackfunc): 
    callbackfunc

def print_red(text: str):
    print(Fore.RED + text + Fore.RESET)

def print_green(text: str):
    print(Fore.GREEN + text + Fore.RESET)

def print_blue(text: str):
    print(Fore.CYAN + text + Fore.RESET)

def absolute_exit():
    os._exit(1)

def check_start():
    if not check_sudo():
        print_red("[E] - This program must be run with superuser privileges!\n")
        absolute_exit()

@animation.wait(d_anim)
def check_requirements():
    unrec = []
    if not cmd_check("fdisk -l"):
        unrec.append(f"{Fore.RED}fdisk{Fore.RESET}\n")
    if not cmd_check("chroot --help"):
        unrec.append(f"{Fore.RED}chroot{Fore.RESET}\n")
    if not cmd_check("usermod -h"):
        unrec.append(f"{Fore.RED}passwd{Fore.RESET}")
    if not unrec == []:
        err_text = f"""\n{Fore.YELLOW}The following dependencies were
not detected on the system,
install them yourself and run
the program again:{Fore.RED}\n"""
        for i in unrec:
            err_text = err_text + i
        next_step(print(err_text))
        absolute_exit()

def scan_disks():
    print_blue("Scanning existing partitions...")
    allparts=os.popen("fdisk -l").read()
    print(allparts)
    print("Type the desired /dev/sda partition (example: /dev/sda1) (type 'quit' to exit)")
    correct_choice = False
    while not correct_choice == True:
        dev_sda_choice = input(f"{Fore.CYAN}>>> {Fore.RESET}")
        if dev_sda_choice.startswith("/dev/") and dev_sda_choice in allparts:
            correct_choice = True
        elif dev_sda_choice == 'quit':
            absolute_exit()
        else:
            print_red("This partition does not exist, try again.")
    return dev_sda_choice

def get_credetionals():
    login = input(f"{Fore.YELLOW}New user name: {Fore.RESET}")
    password = input(f"{Fore.YELLOW}Type password for '{login}': {Fore.RESET}")
    return login, password

@animation.wait('bar', color='blue')
def main_work(partition: str, login: str, password: str):
    path_marker = "/mnt/" + str(uuid4())
    
    if not os.path.exists(path_marker):
        os.makedirs(path_marker)
    
    try:
        print(f"Mounting {partition} to {path_marker}...")
        subprocess.run(['mount', partition, path_marker], check=True)

        print(f"Setting PATH to include /usr/sbin inside chroot...")
        subprocess.run(['chroot', path_marker, 'sh', '-c', 'export PATH=$PATH:/usr/sbin'], check=True)

        print(f"Checking if chpasswd is installed in the chroot environment...")
        try:
            subprocess.run(['chroot', path_marker, 'which', 'chpasswd'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("chpasswd is already installed.")
        except subprocess.CalledProcessError:
            print("chpasswd is not installed. Installing chpasswd...")
            subprocess.run(['chroot', path_marker, 'apt-get', 'update'], check=True)
            subprocess.run(['chroot', path_marker, 'apt-get', 'install', '-y', 'passwd'], check=True)
            print("chpasswd installed successfully.")
        
        print(f"Creating user {login} in chroot environment...")
        subprocess.run(['chroot', path_marker, 'useradd', '-m', '-s', '/bin/bash', login], check=True)

        print(f"Setting password for user {login}...")
        subprocess.run(f"echo '{login}:{password}' | chroot {path_marker} chpasswd", shell=True, check=True)
        print(f"Password for user {login} set successfully.")
        
        print(f"Adding user {login} to the sudo group...")
        subprocess.run(['chroot', path_marker, 'usermod', '-aG', 'sudo', login], check=True)
        print(f"User {login} is now in the sudo group.")

    except subprocess.CalledProcessError as e:
        print_red(f"Error occurred while executing command: {e}")

    finally:
        try:
            print(f"Unmounting {path_marker}...")
            subprocess.run(['umount', path_marker], check=True)
            print(f"Successfully unmounted {path_marker}.")

        except subprocess.CalledProcessError as e:
            if 'device is busy' in str(e):
                print_red(f"Error: {path_marker} is busy. Attempting to find processes using the device...")

                try:
                    subprocess.run(['fuser', '-m', path_marker], check=True)
                    print_red(f"Processes using {path_marker} found. Consider stopping them to proceed with unmounting.")
                except subprocess.CalledProcessError:
                    print_red(f"No processes found using {path_marker}.")

                print("Attempting to force unmount...")
                subprocess.run(['umount', '-l', path_marker], check=True)
                print(f"Successfully force-unmounted {path_marker}.")
            else:
                print_red(f"Error occurred while unmounting: {e}")

        finally:
            if os.path.exists(path_marker):
                os.rmdir(path_marker)
                print(f"Removed the directory {path_marker}")
