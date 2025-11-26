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
Here is the code {{url_for("main.py", "main.py")}}

## Hints
How to enumerate users?

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

||
The /flag url offers a channel for enumerating username via timings attack. 
The idea is to Input a test username, along with a giant password
The key here is knowing that, in 'and' expression...
```username == user and SHA256.new(data=password.encode()).hexdigest() == passHASH```
If username is not equal to user then, the password hash function is not called. 
When the password function is called, the giant password causes the hash function to hang. 
This tells us that we have guessed the right username. 
We can then use that information to submit to /forgetpass and get the password hash
The password becomes really short (3 digits). 
This allows us to either brute force the password using the hash or using a rainbow table.
Here is the solution script {{url_for("solution.py", "solution.py")}}
Remember to modify the BASE_IP_PORT before running solution.py
||
## Attributes
- author: William Lin
- event: RSAC picoCTF

