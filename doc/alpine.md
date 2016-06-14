Alpine linux
=========
For docker os

### command
-------------
```
  add       Add PACKAGEs to 'world' and install (or upgrade) them, while ensuring that all dependencies are met
  del       Remove PACKAGEs from 'world' and uninstall them
  fix       Repair package or upgrade it without modifying main dependencies
  update    Update repository indexes from all remote repositories
  info      Give detailed information about PACKAGEs or repositores, apk info(list all installed packages)
  search    Search package by PATTERNs or by indexed dependencies
  upgrade   Upgrade currently installed packages to match repositories
  cache     Download missing PACKAGEs to cache and/or delete unneeded files from cache
  version   Compare package versions (in installed database vs. available) or do tests on literal version strings
  index     Create repository index file from FILEs
  fetch     Download PACKAGEs from global repositories to a local directory
  audit     Audit the directories for changes
  verify    Verify package integrity and signature
  dot       Generate graphviz graphs
  policy    Show repository policy for packages
  stats     Show statistics about repositories and installations

Global options:
  -h, --help              Show generic help or applet specific help
  -p, --root DIR          Install packages to DIR
  -X, --repository REPO   Use packages from REPO
  -q, --quiet             Print less information
  -v, --verbose           Print more information (can be doubled)
  -i, --interactive       Ask confirmation for certain operations
  -V, --version           Print program version and exit
  -f, --force             Do what was asked even if it looks dangerous
  -U, --update-cache      Update the repository cache
  --progress              Show a progress bar
  --progress-fd FD        Write progress to fd
  --no-progress           Disable progress bar even for TTYs
  --purge                 Delete also modified configuration files (pkg removal) and uninstalled packages from cache (cache clean)
  --allow-untrusted       Install packages with untrusted signature or no signature
  --wait TIME             Wait for TIME seconds to get an exclusive repository lock before failing
  --keys-dir KEYSDIR      Override directory of trusted keys
  --repositories-file REPOFILE Override repositories file
  --no-network            Do not use network (cache is still used)
  --no-cache              Read uncached index from network
  --arch ARCH             Use architecture with --root
  --print-arch            Print default arch and exit
```

### e.g.
-------------
1. install gnuplot package
```
apk add gnuplot \
    --update-cache \
    --repository http://dl-3.alpinelinux.org/alpine/edge/testing/
```
2. show all installed package
```
apk info
apk -vv info | sort   (will list all installed packages in alphabetical order)
```
