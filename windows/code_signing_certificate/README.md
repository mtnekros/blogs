## ✅ Use a **Self-Signed Certificate**, and install it as **Trusted** on factory computers.

This gives you:

* Zero cost (no need to buy from DigiCert or Sectigo)
* Control (you can generate and manage the certificate yourself)
* Security (signed executables can be verified before use)
* Easy deployment (you can install the certificate via GPO, PowerShell, or manual import)

---

## 🔧 Step-by-Step: Sign with a Self-Signed Certificate

### 1. **Create a Self-Signed Code Signing Certificate**

Run this on your dev/build machine:

```powershell
$cert = New-SelfSignedCertificate -Subject "CN=Factory Software Signer" `
  -Type CodeSigningCert `
  -CertStoreLocation "Cert:\CurrentUser\My"
```

### 2. **Export the Certificate (Public + Private)**

```powershell
# Export the full certificate (for signing) as a .pfx with a password
$pwd = ConvertTo-SecureString -String "P@ssw0rd123" -Force -AsPlainText

Export-PfxCertificate -Cert $cert -FilePath "C:\certs\factory_signer.pfx" -Password $pwd
```

### 3. **Export the Public Cert (for installing as trusted)**

```powershell
Export-Certificate -Cert $cert -FilePath "C:\certs\factory_signer.cer"
```

---

### 4. **Use the Certificate to Sign Your EXE**

On your build system (or CI):

```powershell
$pwd = ConvertTo-SecureString -String "P@ssw0rd123" -AsPlainText -Force
$cert = Import-PfxCertificate -FilePath "C:\certs\factory_signer.pfx" `
  -CertStoreLocation Cert:\CurrentUser\My -Password $pwd

Set-AuthenticodeSignature -FilePath "C:\path\to\yourapp.exe" -Certificate $cert
```

---

### 5. **Install the Public Certificate on Factory Computers**

To trust the signature, install `factory_signer.cer` into the **Trusted Root Certification Authorities** store:

#### Option A: PowerShell (run as admin on each factory computer)

```powershell
Import-Certificate -FilePath "C:\certs\factory_signer.cer" `
  -CertStoreLocation "Cert:\LocalMachine\Root"
```

#### Option B: Manually

1. Double-click the `.cer` file.
2. Click **Install Certificate**.
3. Choose **Local Machine**.
4. Store location: **Trusted Root Certification Authorities**.
5. Complete the wizard.

---

## ✅ Done! Now:

* All signed `.exe` files from your factory cert will show a valid signature.
* SmartScreen warnings will be bypassed on those machines (once trusted).
* No external users can use or tamper with the cert.
