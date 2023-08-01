#!/bin/bash

check_installed() {
    command=$1
    if command -v "$command" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

install_package() {
    package=$1
    sudo apt install -y "$package"
}

create_lemp_stack() {
    site_name=$1

    if ! [[ $site_name =~ ^[[:alnum:]]+$ ]]; then
        echo "Site name can only contain letters and numbers."
        exit 1
    fi

    # Add entry to /etc/hosts for example.com
    echo "127.0.0.1 $site_name.com" | sudo tee -a /etc/hosts

    # Define the LEMP stack using Docker Compose
    docker_compose_yml="
version: '3'

services:
  nginx:
    image: nginx:latest
    ports:
      - \"80:80\"
    volumes:
      - ${site_name}_wordpress:/var/www/html
      - ./nginx-conf:/etc/nginx/conf.d
    networks:
      - lemp-network

  php:
    image: php:latest
    volumes:
      - ${site_name}_wordpress:/var/www/html
    networks:
      - lemp-network

  mysql:
    image: mysql:5.7
    environment:
      MYSQL_DATABASE: $site_name
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: wordpress
    volumes:
      - ${site_name}_db:/var/lib/mysql
    networks:
      - lemp-network

volumes:
  ${site_name}_wordpress:
  ${site_name}_db:

networks:
  lemp-network:
"

    # Create a directory for the nginx configuration
    mkdir nginx-conf

    # Write the Docker Compose configuration to a file
    docker_compose_file="docker-compose-${site_name}.yml"
    echo "$docker_compose_yml" | sudo tee "$docker_compose_file" > /dev/null

    # Run the Docker Compose to create the LEMP stack
    sudo docker-compose -f "$docker_compose_file" up -d
    echo "LEMP stack for '${site_name}.com' created successfully."
}

enable_lemp_stack() {
    site_name=$1
    docker_compose_file="docker-compose-${site_name}.yml"
    sudo docker-compose -f "$docker_compose_file" up -d
    echo "LEMP stack for '${site_name}.com' enabled."
}

disable_lemp_stack() {
    site_name=$1
    docker_compose_file="docker-compose-${site_name}.yml"
    sudo docker-compose -f "$docker_compose_file" down
    echo "LEMP stack for '${site_name}.com' disabled."
}

delete_lemp_stack() {
    site_name=$1
    docker_compose_file="docker-compose-${site_name}.yml"
    sudo docker-compose -f "$docker_compose_file" down --volumes

    # Remove the Docker Compose file
    sudo rm "$docker_compose_file"

    # Remove the nginx configuration directory
    sudo rm -rf nginx-conf

    echo "WordPress site '${site_name}.com' and containers deleted successfully."
}

main() {
    required_packages=("docker" "docker-compose")
    missing_packages=()

    for package in "${required_packages[@]}"; do
        if ! check_installed "$package"; then
            missing_packages+=("$package")
        fi
    done

    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        echo "Installing missing packages..."
        for package in "${missing_packages[@]}"; do
            install_package "$package"
        done
        echo "Installation complete."
    fi

    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <subcommand> <site_name>"
        exit 1
    fi

    subcommand=$1
    site_name=$2

    case $subcommand in
    create)
        create_lemp_stack "$site_name"
        ;;
    enable)
        enable_lemp_stack "$site_name"
        ;;
    disable)
        disable_lemp_stack "$site_name"
        ;;
    delete)
        delete_lemp_stack "$site_name"
        ;;
    *)
        echo "Invalid subcommand. Supported subcommands: create, enable, disable, delete"
        exit 1
        ;;
    esac
}

main "$@"
