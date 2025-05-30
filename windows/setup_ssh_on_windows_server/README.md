## 🔐 What Is SSH Key-Based Authentication?

SSH key-based authentication uses a pair of assymetric cryptographic keys:

* **Private Key**: Kept secure on your computer. (Acts like a password)
* **Public Key**: Shared with the server you want to access.

This method is more secure than using passwords, especially when connecting to systems across different networks or domains.

---

## 🛠️ Step-by-Step Setup on Windows

### 1. **Install OpenSSH (if not already installed)**

OpenSSH usually comes installed as far as I know. But incase it isn't, you can
install OpenSSH Client on your computer by following the steps below.

* **Windows 10/11**:
    * Go to **Settings > System > Optional Features**.
    * Click **Add a feature**.
    * For your PC:
        * Search for **OpenSSH Client**, then install it on your PC.
    * If server:
        * Search for **OpenSSH Server**, then install it.
  * Optionally, you can also use PowerShell to install OpenSSH:
    ```powershell
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    ```

### 2. **Start and Configure the SSH Server
* Open PowerShell as Administrator and run:
```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```
* This starts the SSH server and ensures it runs automatically on startup.

### 3. **Generate an SSH Key Pair**
* Open PowerShell or Command Prompt and run:
    ```bash
    ssh-keygen -m PEM -t rsa -b 2048
    ```
    * `-m PEM`: Specifies the key format as PEM.
    * `-t rsa`: Specifies the RSA algorithm.
    * `-b 2048`: Sets the key length to 2048 bits.
* When prompted, press Enter to accept the default file location (`C:\Users\YourName\.ssh\id_rsa`).
* You can also set a passphrase for added security.

### 4. **Copy the Public Key to the Server**
* Locate your public key file (`id_rsa.pub`) in the `.ssh` folder.
* Copy its contents to the `authorized_keys` file on the server:
    * On the server, navigate to `C:\Users\YourName\.ssh\`.
    * Create or open the `authorized_keys` file.
    * Paste the public key content into this file.
* Ensure the `.ssh` folder and `authorized_keys` file have the correct permissions:
    * Only your user account & SYSTEM should have access.
    * Check the permissions with `icacls C:\Users\YourName\.ssh\authorized_keys`
    * Remove all permissions
        ```powershell
        icacls .\authorized_keys /reset # this will reset all manually added permissions
        icacls .\authorized_keys /inheritance:r # this will remove any inherited permissions
        ```
    * Check the permissions again. It should be empty.
    ```powershell
    > icacls C:\Users\YourName\.ssh\authorized_keys
    .\authorized_keys
    Successfully processed 1 files; Failed processing 0 files
    ```
    * Now add only your & SYSTEM access
    ```powershell
    >icacls icacls C:\Users\YourName\.ssh\authorized_keys /grant "YourName:F"
    >icacls icacls C:\Users\YourName\.ssh\authorized_keys /grant "SYSTEM:F"
    ```
    * Check the permissions again. Only you and system should have full access

    ```

### 5. **Connect Using SSH**
* From your client machine, open PowerShell or Command Prompt and run:
    ```bash
    ssh username@hostname
    ```
    * Replace `username` with your server username.
    * Replace `hostname` with the server's IP address or hostname.
* If everything is set up correctly, you'll connect without being prompted for a password.

    ---

## 🔁 Optional: Convert PuTTY `.ppk` Keys to PEM Format
If you have a private key in PuTTY's `.ppk` format and need to convert it to PEM format:
1. Open **PuTTYgen**.
2. Click **Load** and select your `.ppk` file.
3. Go to **Conversions > Export OpenSSH key**.
4. Save the file with a `.pem` extension.

---

👉 [Key-based authentication in OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement)
