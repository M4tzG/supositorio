from dotenv import dotenv_values

def read_env_file(filepath):
    env_values = dotenv_values(filepath)
    env_dict = dict(env_values)
    return env_dict

# # Usage
# env_file = ".env"  # Path to your .env file
# env_dict = read_env_file(env_file)
# print(env_dict)


def DANGEROUS_write_env_file(filepath, env_values):
    with open(filepath, "w") as f:
        for key, value in env_values.items():
            f.write(f"{key}={value}\n")

def update_env_file(filepath, updated_values):
    # Read the existing content of the .env file
    env_values = read_env_file(filepath)

    # Update specific values in the content
    for key, value in updated_values.items():
        env_values[key] = value

    # Write the updated content back to the .env file
    with open(filepath, "w") as f:
        for key, value in env_values.items():
            f.write(f"{key}={value}\n")

# Usage
# env_file = ".env"  # Path to your .env file
# new_env_values = {
#     "LAST_PAGE_STOPPED_AT": "11.5"
# }
# update_env_file(env_file, new_env_values)


# Powered by ChatGPT