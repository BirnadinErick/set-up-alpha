#!/usr/bin/env bash

# Define the output file for the combined backup payload
BACKUP_FILE="$HOME/ssh_backup_payload.txt"

backup_ssh() {
    if [ ! -d "$HOME/.ssh" ]; then
        echo "Error: ~/.ssh directory does not exist."
        exit 1
    fi

    echo "--- SSH BACKUP START ---" > "$BACKUP_FILE"
    
    # Loop through all files in ~/.ssh (excluding known_hosts and authorized_keys)
    for file in "$HOME/.ssh"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            if [[ "$filename" != "known_hosts" && "$filename" != "authorized_keys" ]]; then
                echo "Packing: $filename"
                echo "FILE:$filename" >> "$BACKUP_FILE"
                base64 "$file" >> "$BACKUP_FILE"
                echo "END_FILE" >> "$BACKUP_FILE"
            fi
        fi
    done

    echo "--- SSH BACKUP END ---" >> "$BACKUP_FILE"
    echo "Backup completed. Copy the contents of $BACKUP_FILE into Bitwarden."
}

restore_ssh() {
    local input_payload="$1"

    if [ -z "$input_payload" ] || [ ! -f "$input_payload" ]; then
        echo "Error: Please provide the path to the text file containing the Bitwarden payload."
        echo "Usage: $0 restore /path/to/payload.txt"
        exit 1
    fi

    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"

    local current_file=""
    local inside_file=false
    local encoded_content=""

    while IFS= read -r line; do
        if [[ "$line" == FILE:* ]]; then
            current_file="${line#FILE:}"
            inside_file=true
            encoded_content=""
            echo "Restoring: $current_file"
        elif [[ "$line" == "END_FILE" ]]; then
            if [ -n "$current_file" ]; then
                echo -n "$encoded_content" | base64 -d > "$HOME/.ssh/$current_file"
                # Set strict permissions: 600 for private keys, 644 for public keys
                if [[ "$current_file" == *.pub ]]; then
                    chmod 644 "$HOME/.ssh/$current_file"
                else
                    chmod 600 "$HOME/.ssh/$current_file"
                fi
            fi
            inside_file=false
        elif [ "$inside_file" = true ]; then
            encoded_content+="$line"$'\n'
        fi
    done < "$input_payload"

    echo "Restoration completed successfully."
}

case "$1" in
    backup)
        backup_ssh
        ;;
    restore)
        restore_ssh "$2"
        ;;
    *)
        echo "Usage: $0 {backup|restore /path/to/payload.txt}"
        exit 1
        ;;
esac