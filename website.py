import subprocess
import sys
import os

def check_installed(command):
    try:
        subprocess.run([command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package):
    try:
        subprocess.run(['sudo', 'apt', 'install', '-y', package], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")
        sys.exit(1)

def create_lemp_stack(site_name):
    # Check if the site name contains only valid characters
    if not site_name.isalnum():
        print("Site name can only contain letters and numbers.")
        sys.exit(1)

    # Add entry to /etc/hosts for example.com
    with open('/etc/hosts', 'a') as hosts_file:
        hosts_file.write(f"127.0.0.1\t{site_name}.com\n")

    # Define the LEMP stack using Docker Compose
    docker_compose_yml = f"""
version: '3'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - {site_name}_wordpress:/var/www/html
      - ./nginx-conf:/etc/nginx/conf.d
    networks:
      - lemp-network

  php:
    image: php:latest
    volumes:
      - {site_name}_wordpress:/var/www/html
    networks:
      - lemp-network

  mysql:
    image: mysql:5.7
    environment:
      MYSQL_DATABASE: {site_name}
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: wordpress
    volumes:
      - {site_name}_db:/var/lib/mysql
    networks:
      - lemp-network

volumes:
  {site_name}_wordpress:
  {site_name}_db:

networks:
  lemp-network:
"""

    # Create a directory for the nginx configuration
    subprocess.run(['mkdir', 'nginx-conf'])

    # Write the Docker Compose configuration to a file
    docker_compose_file = f"docker-compose-{site_name}.yml"
    with open(docker_compose_file, 'w') as file:
        file.write(docker_compose_yml)

    # Run the Docker Compose to create the LEMP stack
    subprocess.run(['sudo', 'docker-compose', '-f', docker_compose_file, 'up', '-d'], check=True)
    print(f"LEMP stack for '{site_name}.com' created successfully.")

def enable_lemp_stack(site_name):
    docker_compose_file = f"docker-compose-{site_name}.yml"
    subprocess.run(['sudo', 'docker-compose', '-f', docker_compose_file, 'up', '-d'], check=True)
    print(f"LEMP stack for '{site_name}.com' enabled.")

def disable_lemp_stack(site_name):
    docker_compose_file = f"docker-compose-{site_name}.yml"
    subprocess.run(['sudo', 'docker-compose', '-f', docker_compose_file, 'down'], check=True)
    print(f"LEMP stack for '{site_name}.com' disabled.")

def delete_lemp_stack(site_name):
    docker_compose_file = f"docker-compose-{site_name}.yml"
    subprocess.run(['sudo', 'docker-compose', '-f', docker_compose_file, 'down', '--volumes'], check=True)

    # Remove the Docker Compose file
    subprocess.run(['sudo', 'rm', docker_compose_file], check=True)

    # Remove the nginx configuration directory
    subprocess.run(['sudo', 'rm', '-rf', 'nginx-conf'], check=True)

    print(f"WordPress site '{site_name}.com' and containers deleted successfully.")

def main():
    required_packages = {
        'docker': 'docker',
        'docker-compose': 'docker-compose',
    }

    missing_packages = [package_name for package_name, package_cmd in required_packages.items() if not check_installed(package_cmd)]

    if missing_packages:
        print("Installing missing packages...")
        for package in missing_packages:
            install_package(required_packages[package])
        print("Installation complete.")

    if len(sys.argv) < 3:
        print("Usage: python3 create_lemp_stack.py <subcommand> <site_name>")
        sys.exit(1)

    subcommand = sys.argv[1]
    site_name = sys.argv[2]

    if subcommand == 'create':
        create_lemp_stack(site_name)
    elif subcommand == 'enable':
        enable_lemp_stack(site_name)
    elif subcommand == 'disable':
        disable_lemp_stack(site_name)
    elif subcommand == 'delete':
        delete_lemp_stack(site_name)
    else:
        print("Invalid subcommand. Supported subcommands: create, enable, disable, delete")
        sys.exit(1)

if __name__ == "__main__":
    main()
