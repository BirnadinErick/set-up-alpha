#!/bin/bash

# Default backup file name
BACKUP_FILE="copr_repos_backup.txt"

function backup_copr() {
    echo "Backing up enabled COPR repositories to $BACKUP_FILE..."
    
    # List all COPR repos, filter out disabled ones, keep only the copr lines, 
    # and extract the 'username/projectname' part.
    dnf copr list | grep -v "(disabled)" | grep "copr.fedorainfracloud.org" | sed 's|^copr\.fedorainfracloud\.org/||' > "$BACKUP_FILE"
    
    if [ -s "$BACKUP_FILE" ]; then
        echo "Successfully backed up the following COPR repos:"
        cat "$BACKUP_FILE"
    else
        echo "No enabled COPR repos found or backup failed."
    fi
}

function restore_copr() {
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "Backup file '$BACKUP_FILE' not found!"
        echo "Please run the backup option first on your old system, or ensure the file is in the current directory."
        exit 1
    fi
    
    echo "Restoring COPR repositories from $BACKUP_FILE..."
    while IFS= read -r repo; do
        # Skip empty lines
        if [ -n "$repo" ]; then
            echo "Enabling COPR repo: $repo"
            # Automatically confirm with -y
            sudo dnf copr enable -y "$repo"
        fi
    done < "$BACKUP_FILE"
    echo "Restore complete!"
}

echo "=========================================="
echo "      COPR Backup & Restore Utility       "
echo "=========================================="
echo "1) Backup enabled COPR repos to $BACKUP_FILE"
echo "2) Restore COPR repos from $BACKUP_FILE"
echo "3) Exit"
echo "=========================================="
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        backup_copr
        ;;
    2)
        restore_copr
        ;;
    3)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
