# Password Security 101

This problem demonstrates the notion of the password security game using 
enabling a timing attack based on hash time. The game works as follows:

  1. The user submits username and password to /flag allowing people to obtain the flag
  2. If the username matches, the hash function is then called, causing a the program to run the hash function on the user entered password
  3. if the user entered password is large the program hangs for a split second.
  4. This enables a timing attack on the application, allowing the player to enumerate the username.
  5. The user then can use the username to obtain the hash of a simpler password from /forgetpass
  6. The user can then bruteforce or rainbow table the password to obtain the username and password.
  7. Then the user should submit the username and password to /flag
