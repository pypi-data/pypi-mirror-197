import argparse
import yaml
import requests
import os
import configparser

def orchestrate(filename):
    # Load the API key and secret from the configuration file
    config_file = os.path.join(os.path.expanduser("~"), ".plutis-cli")
    if not os.path.exists(config_file):
        print("Please authenticate first using 'plutis authenticate --api_key <api_key> --api_secret <api_secret>'")
        return

    config = configparser.ConfigParser()
    config.read(config_file)
    api_key = config.get("plutis", "api_key")
    api_secret = config.get("plutis", "api_secret")

    # Read the YAML file
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    # Send the dictionary as a POST request
    url = "https://api.plutis.io/api/v1/orchestration/create"
    headers = {
        "x-api-key": api_key,
        "x-api-secret": api_secret,
    }
    response = requests.post(url, json=data, headers=headers)

    # Print the response
    if response.status_code == 200:
        print("Orchestration created successfully")
    else:
        print(f"Error: {response.text}")

def authenticate(api_key, api_secret):
    config = configparser.ConfigParser()
    config["plutis"] = {"api_key": api_key, "api_secret": api_secret}

    config_file = os.path.join(os.path.expanduser("~"), ".plutis-cli")
    with open(config_file, "w") as file:
        config.write(file)

    print("API key and secret saved successfully.")

def main():
    parser = argparse.ArgumentParser(description="Plutis CLI tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # Orchestrate command
    orchestrate_parser = subparsers.add_parser("orchestrate", help="Process a YAML file and send the contents as a dictionary to the Plutis API")
    orchestrate_parser.add_argument("--yaml", type=str, required=True, help="The YAML file to process")

    # Authenticate command
    authenticate_parser = subparsers.add_parser("authenticate", help="Register the API key and secret")
    authenticate_parser.add_argument("--api_key", type=str, required=True, help="The API key")
    authenticate_parser.add_argument("--api_secret", type=str, required=True, help="The API secret")

    args = parser.parse_args()

    if args.command == "orchestrate":
        orchestrate(args.yaml)
    elif args.command == "authenticate":
        authenticate(args.api_key, args.api_secret)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
