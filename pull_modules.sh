cd modules
find . -mindepth 1 -maxdepth 1 -type d -not -name "example_module" -exec git --git-dir={}/.git --work-tree=$PWD/{} pull origin master \;