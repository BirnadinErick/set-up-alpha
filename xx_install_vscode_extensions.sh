#! /usr/bin/env bash

extensions=(
	platformio.platformio-ide
	ms-python.python
	ms-vscode.cpptools
	Gruntfuggly.todo-tree
	vscodevim.vim
)

for extension in "${extensions[@]}"; do
    code --install-extension "$extension"
done
