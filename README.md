# SetUp Alpha

> alpha is a codename i use for a computer that act as central actor on my home network

these scripts are intented to run on every major release of Fedora(the distro i use currently).
this sets up a foundation that i can further enhance.

# How to use

First, make the scripts executable:

```sh
chmod +x 0*.sh
```

then run them in order:

```sh
./files.sh
```

this will create a list of files in the directory that can be copied into run.sh script.

Now go into run.sh script and delete the files that you do not wish to run, and save it.

```sh
./run.sh
```
