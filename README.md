# LEMP Stack Setup for WordPress with Docker

This command-line script allows you to create, enable, disable, and delete a LEMP (Linux, Nginx, MySQL, PHP) stack for hosting a WordPress site using Docker. The script checks for required packages (Docker and Docker Compose) and installs them if missing.

## Prerequisites

Before running the script, ensure that you have the following prerequisites installed on your system:

1. Docker: Make sure you have Docker installed and configured on your machine.
   - You can install Docker from the official Docker website: https://www.docker.com/get-started

2. Docker Compose: Verify that you have Docker Compose installed on your system.
   - If not installed, you can install Docker Compose following the instructions from: https://docs.docker.com/compose/install/

## Usage

To use the script, follow the steps below:

1. Clone this repository or download the `website.py` script to your local machine.

2. Open a terminal (command prompt) on your system.

3. Navigate to the directory where the `website.py` script is located.

4. Run the script with the following syntax:




- `<subcommand>`: Specify one of the supported subcommands (`create`, `enable`, `disable`, or `delete`).
- `<site_name>`: Provide the desired name for the WordPress site. It should contain only letters and numbers.

## Subcommands

1. `create`: Creates a LEMP stack for the specified site name.
- Example: `python3 website.py create example.com`

2. `enable`: Enables (starts) the existing LEMP stack for the specified site name.
- Example: `python3 website.py enable example.com`

3. `disable`: Disables (stops) the existing LEMP stack for the specified site name.
- Example: `python3 website.py disable example.com`

4. `delete`: Deletes the existing LEMP stack for the specified site name.
- Example: `python3 website.py delete example.com`

Please note that this script assumes you have appropriate permissions to run Docker commands with `sudo`.

## Example

1. Create LEMP Stack
```bash 
sudo python3 website.py create example.com
```
2. Enable/Disable LEMP Stack
```bash
sudo python3 website.py enable example.com
```
```bash
sudo python3 website.py disable example.com
```

3. Delete LEMP Stack
```bash 
sudo python3 website.py delete example.com
```
4. Now, you should be able to access the website using the site name example.com in your web browser. Open your web browser and enter the following URL:
```bash
http://example.com
```

