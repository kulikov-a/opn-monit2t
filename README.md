A simple OPNsense plugin that sends Monit alerts to a Telegram bot.

ref. https://forum.opnsense.org/index.php?topic=36805.0

![image](https://github.com/user-attachments/assets/14e34337-5785-47cb-927c-af1baf891453)

## Install

The package contains no native binaries. It is stamped `FreeBSD:*:*`, so the same file installs on FreeBSD 14 and FreeBSD 15.

```
pkg add https://github.com/kulikov-a/opn-monit2t/raw/main/work/pkg/os-monit2t-1.3.pkg
```

Then open Services → Monit → Telegram.

Monit needs an Execute action with this path:

```
/usr/local/opnsense/scripts/OPNsense/Monit2T/monit2t.sh
```

## Rebuild

`PLUGIN_NO_ABI` is set so a later `make package` does not pin the archive to the build machine. On an OPNsense box:

```
opnsense-code plugins
cp -a . /usr/plugins/sysutils/monit2t
cd /usr/plugins/sysutils/monit2t
make package
```

`tools/stamp-noabi.py` rewrites `abi` / `arch` on an already built `.pkg` when that build ran without `PLUGIN_NO_ABI`.
