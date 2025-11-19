# PASSSEC
  - Namespace: picoctf
  - ID: passsec
  - Type: custom
  - Category: Web
  - Points: 200
  - Templatable: yes

## Description

Password length is crucial for security. However, have you actually tried cracking the hash of a weak password?


## Details

The Password Security game is running at {{link_as('/', 'here')}}.

## Hints
What are rainbow tables?

## Tags
 - beginner

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Solution Overview

willi@LAPTOP-T2EUIAOQ:~/ctf-problemdev/challenges$ cp -r problem-dev/ ~/cmgr/challenges/ && cmgr update && cmgr playtest picoctf/passsec
Updated:
    picoctf/passsec
cmgr: [WARN:  disk quota for picoctf/passsec container 'challenge' ignored (disk quotas are not enabled)]
challenge information available at: http://localhost:4242/

## Attributes
- author: William Lin
- event: RSAC picoCTF

